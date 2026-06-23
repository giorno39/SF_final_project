from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils.timezone import now

from final_project.accounts.models import Specialization
from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper, TermPaperRequest
from final_project.trophies.models import Trophy
from final_project.useful_materials.models import MaterialComment, Materials

UserModel = get_user_model()


def create_trophies_for_teacher(user, count=2):
    result = [Trophy(
        rate=1 + i,
        project=f'DB{i}',
        obtained_at=now(),
        completed_by=user
    ) for i in range(1, count + 1)]

    [t.save() for t in result]

    return result

def create_term_paper_for_1_user(user, date=now(), taken=None):
    paper = TermPaper.objects.create(
        title='title',
        university='uni',
        death_line=date,
        description='asdasd',
        content='term_paper_files/dummy.txt_2PLPA4x.txt',
        user_id=user.pk,
        price_cap=22,
        taken_by=taken,
    )

    return paper

def create_term_papers_for_2_users(user1, user2, count=5):
    # Creates 3 term_papers for user2, and 2 papers for user1
    result = [TermPaper(
        title=f'title{i}',
        university=f'uni{i}',
        death_line=now(),
        description='asdasd',
        content=f'term_paper_files/dummy.txt_9{i}5yBt.txt',
        user_id=user1.pk if i % 2 == 0 else user2.pk,
        price_cap=22,
        taken_by=user1
    ) for i in range(count)]

    [t.save() for t in result]

    return result


def create_completed_term_paper(user, count=2):
    result = [TermPaper(
        title=f'title{i}',
        university=f'uni{i}',
        death_line=now(),
        description='asdasd',
        content=f'term_paper_files/dummy.txt_9{i}5yBt.txt',
        user_id=user.pk,
        price_cap=22,
        completed=True,
        taken_by=user,
    ) for i in range(count)]

    [t.save() for t in result]

    return result


def create_lessons_from_2_users(user1, user2, count=3):
    # 2 lessons for user 1 and one for user 2 by default
    result = [Lesson(
        title=f'demo{i}',
        price=30,
        teacher_id=user1.pk if i % 2 == 0 else user2.pk
    ) for i in range(count)]

    [l.save() for l in result]

    return result


def create_lesson_for_1_user(user):
    lesson = Lesson.objects.create(
        title='demo',
        price=30,
        teacher_id=user.pk
    )

    return lesson


def create_material_for_1_user(user):
    material = Materials.objects.create(
        title='demo',
        references='https://en.wikipedia.org/wiki/Japanese_language',
        uploaded_by=user
    )

    return material


# --- Helpers added for the extended test suite ---------------------------------

def create_user(user_type='student', suffix='', **overrides):
    """Create (without logging in) a user of the requested type.

    The username/email are made unique via ``suffix`` so several users can be
    created inside the same test.
    """
    data = {
        'username': f'user_{user_type}{suffix}',
        'password': 'test_pass',
        'email': f'user_{user_type}{suffix}@abv.bg',
        'user_type': user_type,
    }
    data.update(overrides)
    return UserModel.objects.create_user(**data)


def create_specialization(name='Mathematics'):
    specialization, _ = Specialization.objects.get_or_create(name=name)
    return specialization


def create_active_term_paper(user, days_until_deadline=30, **overrides):
    """A term paper that should appear in the public discovery feed:
    not taken, not completed and with a future deadline."""
    data = dict(
        title='active title',
        university='uni',
        death_line=now().date() + timedelta(days=days_until_deadline),
        description='desc',
        content='term_paper_files/dummy.txt',
        user_id=user.pk,
        price_cap=22,
        taken_by=None,
        completed=False,
    )
    data.update(overrides)
    return TermPaper.objects.create(**data)


def create_term_paper_request(term_paper, student, teacher,
                              status=TermPaperRequest.StatusChoices.PENDING):
    return TermPaperRequest.objects.create(
        term_paper=term_paper,
        student=student,
        teacher=teacher,
        status=status,
    )


def create_material_comment(material, author, content='nice material'):
    return MaterialComment.objects.create(
        material=material,
        author=author,
        content=content,
    )
