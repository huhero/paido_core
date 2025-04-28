FROM python:3.12-slim
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10

# RUN poetry install --without dev --no-interaction --no-ansi
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
# CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "paido_core.app:app"]
CMD ["poetry", "run", "fastapi", "run", "--host", "0.0.0.0", "src/paido_core/app.py"]