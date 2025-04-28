from jwt import decode

from paido_core.security import create_access_token
from paido_core.settings import Settings

settings = Settings()


def test_security_create_access_token():
    data = {'sub': 'test@test.com'}
    token = create_access_token(data)

    decoded = decode(
        token, settings.SECRET_JWT_KEY, algorithms=[settings.ALGORITHM_JWT]
    )

    assert decoded['sub'] == data['sub']
    assert 'exp' in decoded
