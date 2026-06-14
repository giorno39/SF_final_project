import json
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from final_project.ai.client import get_openai_client


BLOCKED_KEYWORDS = [
    'porn',
    'casino',
    'bet',
    'betting',
    'gambling',
    'xxx',
    'escort',
    'adult',
    'webcam',
]

def _fallback_validate_reference(url, specialization_names, preview):
    combined_text = normalize_text(
        ' '.join([
            preview.get('title', ''),
            preview.get('meta_description', ''),
            preview.get('text_excerpt', ''),
        ])
    ).lower()

    normalized_specializations = [
        normalize_text(name).lower()
        for name in specialization_names
        if normalize_text(name)
    ]

    matched_specializations = [
        name
        for name in specialization_names
        if normalize_text(name).lower() in combined_text
    ]

    is_relevant = bool(matched_specializations)

    if not normalized_specializations:
        is_relevant = True

    if not is_relevant:
        return {
            'is_allowed': False,
            'is_safe': True,
            'is_relevant': False,
            'matched_specializations': [],
            'reason': 'The reference appears safe, but it does not clearly match the selected specializations.',
            'preview': preview,
        }

    return {
        'is_allowed': True,
        'is_safe': True,
        'is_relevant': True,
        'matched_specializations': matched_specializations,
        'reason': 'Reference accepted using fallback validation because AI validation is unavailable.',
        'preview': preview,
    }


def normalize_text(value):
    return ' '.join((value or '').split()).strip()


def is_obviously_blocked_url(url):
    lowered = url.lower()
    return any(keyword in lowered for keyword in BLOCKED_KEYWORDS)


def fetch_reference_preview(url, timeout=8):
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MaterialReferenceValidator/1.0)',
    }

    response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
    response.raise_for_status()

    content_type = response.headers.get('Content-Type', '').lower()
    if 'text/html' not in content_type:
        return {
            'final_url': response.url,
            'title': '',
            'meta_description': '',
            'text_excerpt': '',
            'content_type': content_type,
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    title = normalize_text(soup.title.string if soup.title and soup.title.string else '')

    meta_description = ''
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    if meta_tag and meta_tag.get('content'):
        meta_description = normalize_text(meta_tag['content'])

    body_text = normalize_text(soup.get_text(separator=' ', strip=True))
    text_excerpt = body_text[:3000]

    return {
        'final_url': response.url,
        'title': title,
        'meta_description': meta_description,
        'text_excerpt': text_excerpt,
        'content_type': content_type,
    }


def validate_reference_with_ai(url, specialization_names):
    parsed = urlparse(url)

    if parsed.scheme not in ('http', 'https'):
        return {
            'is_allowed': False,
            'reason': 'Only http and https links are allowed.',
        }

    if is_obviously_blocked_url(url):
        return {
            'is_allowed': False,
            'reason': 'This link appears to contain blocked or unsafe content.',
        }

    try:
        preview = fetch_reference_preview(url)
    except requests.RequestException:
        return {
            'is_allowed': False,
            'reason': 'The reference could not be reached or read.',
        }

    if not preview['text_excerpt'] and 'html' not in preview['content_type']:
        return {
            'is_allowed': False,
            'reason': 'The reference must point to a readable web page.',
        }

    client = get_openai_client()

    if client is None:
        return _fallback_validate_reference(
            url=url,
            specialization_names=specialization_names,
            preview=preview,
        )

    prompt = f"""
You are validating whether a submitted educational reference link is acceptable for an academic materials platform.

Selected specializations:
{', '.join(specialization_names) if specialization_names else 'None provided'}

Reference URL:
{url}

Final fetched URL:
{preview['final_url']}

Page title:
{preview['title']}

Meta description:
{preview['meta_description']}

Page excerpt:
{preview['text_excerpt']}

Rules:
1. Reject pornography, adult content, escorts, gambling, betting, casinos, scams, malware, phishing, or dangerous unrelated content.
2. Reject content that is clearly unrelated to academic or educational use.
3. Approve only if the page appears safe and reasonably relevant to at least one of the selected specializations.
4. Be strict. If uncertain, reject.

Return ONLY valid JSON in this format:
{{
  "is_allowed": true or false,
  "is_safe": true or false,
  "is_relevant": true or false,
  "matched_specializations": ["..."],
  "reason": "short explanation"
}}
""".strip()

    try:
        response = client.responses.create(
            model='gpt-4.1-mini',
            input=prompt,
        )
    except Exception:
        return _fallback_validate_reference(
            url=url,
            specialization_names=specialization_names,
            preview=preview,
        )

    raw_output = response.output_text.strip()

    try:
        result = json.loads(raw_output)
    except json.JSONDecodeError:
        return {
            'is_allowed': False,
            'reason': 'Reference validation failed. Please try another link.',
        }

    return {
        'is_allowed': bool(result.get('is_allowed')),
        'is_safe': bool(result.get('is_safe')),
        'is_relevant': bool(result.get('is_relevant')),
        'matched_specializations': result.get('matched_specializations', []),
        'reason': result.get('reason', 'This reference was rejected.'),
        'preview': preview,
    }