from sqlalchemy import select

from paido_core.models.user import User


def test_model_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()
    # session.refresh(new_user)
    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
