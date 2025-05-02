from http import HTTPStatus

from paido_core.schemas.user import UserPublic


def test_create_user(client):
    response = client.post(
        url='/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_already_exists(client, user):
    response = client.post(
        url='/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code != HTTPStatus.OK
    # assert response.json() == {'message': 'User already registered'}


def test_read_users(client):
    response = client.get(url='/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get(url='/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_username(client, user):
    response = client.get(url=f'/users/{user.username}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_read_user_by_username_not_found(client):
    response = client.get('/users/wrong_username')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, user, token):
    response = client.put(
        url=f'/users/{user.username}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_update_wrong_user(client, other_user, token):
    response = client.put(
        url=f'/users/{other_user.username}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'hola',
            'email': 'hola@example.com',
            'password': 'hola',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_update_user_wrong_token(client, user):
    response = client.put(
        url=f'/users/{user.username}',
        headers={'Authorization': 'Bearer TOKEN_ERRADO'},
        json={
            'username': 'hola',
            'email': 'hola@example.com',
            'password': 'hola',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user(client, user, token):
    response = client.delete(
        url=f'/users/{user.username}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(
        url=f'/users/{other_user.username}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user_wrong_token(client, user):
    response = client.delete(
        url=f'/users/{user.username}',
        headers={'Authorization': 'Bearer TOKEN_ERRADO'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
