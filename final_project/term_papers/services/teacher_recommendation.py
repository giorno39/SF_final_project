from statistics import mean
import json
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Prefetch

from final_project.accounts.models import TeacherProfile
from final_project.completed_papers.models import CompletedPaper
from final_project.trophies.models import Trophy
from django.conf import settings

from final_project.ai.client import get_openai_client

UserModel = get_user_model()

DEBUG_EMPTY_AI_SENTINEL = True

def _safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize(value, max_value):
    if not max_value:
        return 0.0
    return min(_safe_float(value) / max_value, 1.0)


def _get_term_paper_specialization_names(term_paper):
    return {
        spec.name.strip().lower()
        for spec in term_paper.specializations.all()
        if spec.name
    }


def _get_teacher_specialization_names(profile):
    return {
        spec.name.strip().lower()
        for spec in profile.specializations.all()
        if spec.name
    }


def _get_relevant_completed_papers(completed_papers, term_paper_spec_names):
    relevant = []

    for paper in completed_papers:
        paper_spec_names = {
            spec.name.strip().lower()
            for spec in paper.specializations.all()
            if spec.name
        }

        if term_paper_spec_names.intersection(paper_spec_names):
            relevant.append(paper)

    return relevant


def build_teacher_candidate(profile, term_paper):
    teacher = profile.user
    term_paper_spec_names = _get_term_paper_specialization_names(term_paper)
    teacher_spec_names = _get_teacher_specialization_names(profile)

    specialization_overlap = len(term_paper_spec_names.intersection(teacher_spec_names))
    specialization_score = (
        specialization_overlap / max(len(term_paper_spec_names), 1)
    )

    completed_papers = list(
        CompletedPaper.objects.filter(completed_by=teacher).prefetch_related("specializations")
    )
    relevant_completed_papers = _get_relevant_completed_papers(
        completed_papers,
        term_paper_spec_names,
    )

    trophies = list(Trophy.objects.filter(completed_by=teacher))
    avg_trophy_rate = mean([t.rate for t in trophies]) if trophies else 0.0

    trust_score_normalized = _normalize(profile.trust_score, 100)
    trophy_score_normalized = _normalize(avg_trophy_rate, 5)
    experience_score_normalized = min(len(relevant_completed_papers) / 5, 1.0)

    base_score = (
        0.45 * specialization_score +
        0.30 * trust_score_normalized +
        0.15 * trophy_score_normalized +
        0.10 * experience_score_normalized
    )

    return {
        "teacher_id": teacher.pk,
        "teacher_name": teacher.get_full_name() or teacher.username,
        "email": teacher.email,
        "trust_score": profile.trust_score,
        "specializations": [spec.name for spec in profile.specializations.all()],
        "specialization_overlap": specialization_overlap,
        "avg_trophy_rate": round(avg_trophy_rate, 2),
        "trophy_count": len(trophies),
        "completed_papers_count": len(completed_papers),
        "relevant_completed_papers_count": len(relevant_completed_papers),
        "completed_papers": [
            {
                "title": paper.title,
                "description": getattr(paper, "description", "") or "",
                "specializations": [spec.name for spec in paper.specializations.all()],
            }
            for paper in completed_papers[:5]
        ],
        "recent_trophies": [
            {
                "project": trophy.project or "",
                "rate": trophy.rate,
                "comment": trophy.comment or "",
            }
            for trophy in trophies[:5]
        ],
        "base_score": round(base_score, 4),
    }


def get_pre_ranked_teacher_candidates(term_paper, shortlist_size=8):
    teacher_profiles = (
        TeacherProfile.objects
        .select_related("user")
        .prefetch_related("specializations")
    )

    candidates = [
        build_teacher_candidate(profile, term_paper)
        for profile in teacher_profiles
    ]

    candidates.sort(key=lambda x: x["base_score"], reverse=True)
    return candidates[:shortlist_size]


def rank_teachers_with_ai(term_paper, shortlist_size=8, result_size=3):
    candidates = get_pre_ranked_teacher_candidates(
        term_paper=term_paper,
        shortlist_size=shortlist_size,
    )

    if not candidates:
        return []

    client = get_openai_client()

    prompt_payload = {
        "term_paper": {
            "id": term_paper.pk,
            "title": term_paper.title,
            "description": term_paper.description or "",
            "specializations": [spec.name for spec in term_paper.specializations.all()],
            "university": term_paper.university,
            "deadline": str(term_paper.death_line),
        },
        "teachers": candidates,
        "task": (
            f"Rank the best {result_size} teachers for this term paper. "
            f"There are {len(candidates)} candidate teachers available. "
            "You must return at least 1 recommendation and at most "
            f"{min(result_size, len(candidates))}. "
            "Do not return an empty recommendations list if any teachers are provided. "
            "If no teacher is a perfect fit, return the best available matches anyway. "
            "Use semantic similarity between the paper topic and teacher background, "
            "but also consider trust score, trophy ratings, and relevant completed papers."
        ),
    }

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are helping rank teachers for a university term paper platform. "
                    "Return valid JSON only. "
                    "Do not include markdown fences. "
                    "Do not include commentary outside the JSON. "
                    "Prefer teachers whose background, past completed papers, and reputation "
                    "best match the term paper."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Return JSON with this exact shape:\n"
                    "{\n"
                    '  "recommendations": [\n'
                    "    {\n"
                    '      "teacher_id": 1,\n'
                    '      "rank": 1,\n'
                    '      "score": 92,\n'
                    '      "reason": "One short sentence."\n'
                    "    }\n"
                    "  ]\n"
                    "}\n\n"
                    "Rules:\n"
                    f"- You have {len(candidates)} available teachers.\n"
                    f"- Return between 1 and {min(result_size, len(candidates))} recommendations.\n"
                    "- Never return an empty recommendations array when teachers are provided.\n"
                    "- Pick the best available matches even if the fit is imperfect.\n"
                    "- Return valid JSON only.\n\n"
                    f"Here is the data:\n{json.dumps(prompt_payload, ensure_ascii=False)}"
                ),
            },
        ],
    )

    raw_text = (response.output_text or "").strip()

    print("RAW AI TEXT:", repr(raw_text))
    print("CANDIDATE IDS:", [candidate["teacher_id"] for candidate in candidates])

    if not raw_text:
        if DEBUG_EMPTY_AI_SENTINEL:
            return _build_ai_debug_recommendation(
                "empty-output",
                "DEBUG: response.output_text was empty.",
            )
        return []

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        if DEBUG_EMPTY_AI_SENTINEL:
            return _build_ai_debug_recommendation(
                "invalid-json",
                f"DEBUG: json.loads failed. Raw text: {raw_text[:180]}",
            )
        return []

    recommendations = parsed.get("recommendations", [])

    print("PARSED RECOMMENDATIONS:", recommendations)

    if not isinstance(recommendations, list):
        if DEBUG_EMPTY_AI_SENTINEL:
            return _build_ai_debug_recommendation(
                "wrong-shape",
                "DEBUG: Parsed JSON, but recommendations was not a list.",
            )
        return []

    cleaned_recommendations = []

    candidate_map = {
        candidate["teacher_id"]: candidate
        for candidate in candidates
    }

    for item in recommendations[:result_size]:
        if not isinstance(item, dict):
            continue

        teacher_id = item.get("teacher_id")
        print("AI teacher_id before cast:", teacher_id, type(teacher_id))

        try:
            teacher_id = int(teacher_id)
        except (TypeError, ValueError):
            continue

        if teacher_id not in candidate_map:
            continue

        candidate = candidate_map[teacher_id]

        cleaned_recommendations.append({
            "teacher_id": teacher_id,
            "teacher_name": candidate["teacher_name"],
            "email": candidate["email"],
            "specializations": candidate["specializations"],
            "trust_score": candidate["trust_score"],
            "avg_trophy_rate": candidate["avg_trophy_rate"],
            "trophy_count": candidate["trophy_count"],
            "completed_papers_count": candidate["completed_papers_count"],
            "relevant_completed_papers_count": candidate["relevant_completed_papers_count"],
            "base_score": candidate["base_score"],
            "rank": item.get("rank"),
            "score": item.get("score"),
            "reason": item.get("reason", "").strip(),
        })

    if not cleaned_recommendations:
        if DEBUG_EMPTY_AI_SENTINEL:
            return _build_ai_debug_recommendation(
                "candidate-mismatch",
                "DEBUG: AI returned recommendations, but none matched backend candidate IDs.",
            )
        return []

    cleaned_recommendations.sort(
        key=lambda x: (x["rank"] is None, x["rank"])
    )

    return cleaned_recommendations


def _build_ai_debug_recommendation(code, reason):
    return [{
        "teacher_id": -99999,
        "teacher_name": f"DEBUG: {code}",
        "email": f"{code}@debug.local",
        "specializations": ["DEBUG"],
        "trust_score": 0,
        "avg_trophy_rate": 0,
        "trophy_count": 0,
        "completed_papers_count": 0,
        "relevant_completed_papers_count": 0,
        "base_score": 0,
        "rank": 1,
        "score": 0,
        "reason": reason,
    }]