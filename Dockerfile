FROM python:3.7
RUN pip install fastapi uvicorn poetry flask flask_awscognito
COPY pyproject.toml poetry.lock ./
RUN  poetry install --no-root
# Copy in everything else:
COPY . .
RUN poetry install
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
