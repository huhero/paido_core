from http import HTTPStatus

from tests.conftest import CourseFactory, SchoolFactory


def test_create_course(session, client, token, user):
    school = SchoolFactory(user_id=user.id)
    session.add(school)
    session.commit()
    session.refresh(school)

    response = client.post(
        url=f'/school/{school.id}/course',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Course Test',
            'description': 'Description Test',
            'school_id': school.id,
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'name': 'Course Test',
        'description': 'Description Test',
    }


def test_create_duplicate_course(session, client, token, user):
    school = SchoolFactory(user_id=user.id)
    session.add(school)
    session.commit()
    session.refresh(school)

    response = client.post(
        url=f'/school/{school.id}/course',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Course Test',
            'description': 'Description Test',
            'school_id': school.id,
        },
    )

    response = client.post(
        url=f'/school/{school.id}/course',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Course Test',
            'description': 'Description Test',
            'school_id': school.id,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Your course already exists'}


def test_create_course_without_school(client, token):
    fake_school_id = 99999
    response = client.post(
        url=f'/school/{fake_school_id}/course',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'Course Test',
            'description': 'Description Test',
            'school_id': fake_school_id,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'There is no school for this course.'}


def test_get_course(session, client, token, user):
    school = SchoolFactory(user_id=user.id)
    session.add(school)
    session.commit()
    session.refresh(school)

    course = CourseFactory(school_id=school.id)
    session.add(course)
    session.commit()
    session.refresh(course)
    response = client.get(
        url=f'/school/{school.id}/course/{course.name}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': course.id,
        'name': course.name,
        'description': course.description,
    }


def test_get_course_not_found(session, client, token, user):
    school = SchoolFactory(user_id=user.id)
    session.add(school)
    session.commit()
    session.refresh(school)

    course = CourseFactory(school_id=school.id)
    session.add(course)
    session.commit()
    session.refresh(course)

    response = client.get(
        url=f'/school/{school.id}/course/invalid_course_name',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Course not found'}


def test_get_course_without_school(client, token):
    fake_school_id = 99999
    response = client.get(
        url=f'/school/{fake_school_id}/course/invalid_course_name',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'There is no school for this course.'}
