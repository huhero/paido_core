from http import HTTPStatus

from fastapi import FastAPI

from paido_core.routers import auth, schools, users
from paido_core.schemas import Message

app = FastAPI()
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(schools.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hola mundo!'}
