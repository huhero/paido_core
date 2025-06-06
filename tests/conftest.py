import factory
import factory.fuzzy
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from paido_core.app import app
from paido_core.core.security import get_password_hash
from paido_core.db.session import get_session
from paido_core.models import table_registry
from paido_core.models.course import Course
from paido_core.models.school import School, SchoolType
from paido_core.models.user import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}$SECRET')


class SchoolFactory(factory.Factory):
    class Meta:
        model = School

    name = factory.Faker('name')
    address = factory.Faker('address')
    phone = factory.Faker('phone_number')
    school_type = factory.fuzzy.FuzzyChoice(SchoolType)
    user_id = 1


class CourseFactory(factory.Factory):
    class Meta:
        model = Course

    name = factory.Faker('name')
    description = factory.Faker('text')
    school_id = 1


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())
        with _engine.begin():
            yield _engine


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
        session.rollback()

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    pwd = 'testtest'
    user = UserFactory(password=get_password_hash(pwd))
    session.add(user)
    session.commit()
    session.refresh(user)
    user.clean_password = pwd

    return user


@pytest.fixture
def other_user(session):
    user = UserFactory()
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        url='/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    return response.json()['access_token']
