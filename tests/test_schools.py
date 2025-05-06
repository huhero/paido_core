from http import HTTPStatus

from tests.conftest import SchoolFactory


def test_create_school(client, token):
    response = client.post(
        url='/schools/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'School Test',
            'address': 'Address Test',
            'phone': '+9876543',
            'school_type': 'school',
        },
    )

    assert response.json() == {
        'id': 1,
        'name': 'School Test',
        'address': 'Address Test',
        'phone': '+9876543',
        'school_type': 'school',
    }


def test_list_schools_should_return_3_schools(session, client, user, token):
    expected_schools = 3
    session.bulk_save_objects(
        SchoolFactory.create_batch(expected_schools, user_id=user.id)
    )
    session.commit()
    response = client.get(
        url='/schools', headers={'Authorization': f'Bearer {token}'}
    )

    assert len(response.json()) == expected_schools


def test_list_schools_offset_and_limit(session, client, user, token):
    expected_schools = 2
    session.bulk_save_objects(SchoolFactory.create_batch(10, user_id=user.id))
    session.commit()
    response = client.get(
        url='/schools?ofsset=0&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()) == expected_schools


def test_list_schools_by_name(session, client, user, token):
    expected_schools = 1
    session.bulk_save_objects(SchoolFactory.create_batch(10, user_id=user.id))
    session.bulk_save_objects(
        SchoolFactory.create_batch(1, user_id=user.id, name='escuela')
    )
    session.commit()
    response = client.get(
        url='/schools?name=escu',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()) == expected_schools


def test_delete_school(session, client, user, token):
    school = SchoolFactory(user_id=user.id)
    session.add(school)
    session.commit()
    session.refresh(school)

    response = client.delete(
        url=f'/schools/{school.name}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'School has been deleted successfully.'
    }


def test_delete_wrong_school(client, token):
    response = client.delete(
        url='/schools/10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'School not found.'}


def test_patch_school(session, client, user, token):
    school = SchoolFactory(user_id=user.id)

    session.add(school)
    session.commit()
    session.refresh(school)

    response = client.patch(
        url=f'/schools/{school.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'teste'},
    )

    assert response.status_code == HTTPStatus.OK
    # assert response.json()['name'] == 'teste'


def test_patch_wrong_school(client, token):
    response = client.patch(
        url='/schools/10',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'teste'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'School not found.'}
