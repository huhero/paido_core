from http import HTTPStatus

from fastapi import FastAPI

from paido_core.routers import (
    auth_router,
    course_router,
    schools_router,
    users_router,
)
from paido_core.schemas.message import Message

app = FastAPI()
app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(schools_router.router)
app.include_router(course_router.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hola mundo!'}
