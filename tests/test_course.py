from http import HTTPStatus

from tests.conftest import SchoolFactory


def test_create_school(session, client, token, user):
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


# def test_create_same_school(client, token):
#     response = client.post(
#         url='/schools/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'name': 'School Test',
#             'address': 'Address Test',
#             'phone': '+9876543',
#             'school_type': 'school',
#         },
#     )
#     response = client.post(
#         url='/schools/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={
#             'name': 'School Test',
#             'address': 'Address Test',
#             'phone': '+9876543',
#             'school_type': 'school',
#         },
#     )

#     assert response.status_code == HTTPStatus.BAD_REQUEST
#     assert response.json() == {'detail': 'School already registered'}
