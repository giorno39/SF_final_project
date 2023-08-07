from django.utils.timezone import now

from final_project.lessons.models import Lesson
from final_project.term_papers.models import TermPaper
from final_project.trophies.models import Trophy
from final_project.useful_materials.models import Materials


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
        subject='sub',
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
        subject=f'sub{i}',
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
        subject=f'sub{i}',
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
        subject=f'demo{i}',
        price=30,
        teacher_id=user1.pk if i % 2 == 0 else user2.pk
    ) for i in range(count)]

    [l.save() for l in result]

    return result


def create_lesson_for_1_user(user):
    lesson = Lesson.objects.create(
        title='demo',
        subject='demo',
        price=30,
        teacher_id=user.pk
    )

    return lesson


def create_material_for_1_user(user):
    material = Materials.objects.create(
        title='demo',
        field='demo',
        references='https://en.wikipedia.org/wiki/Japanese_language',
        uploaded_by=user
    )

    return material