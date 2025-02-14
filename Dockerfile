FROM python:3.12

LABEL maintainer=hasnainaskari32@gmail.com

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY . /app/

RUN poetry config virtualenvs.create false

# Ensure Streamlit is installed
RUN poetry install --no-root  # No-root ensures it installs all dependencies

EXPOSE 8000 8501

CMD ["sh", "-c", "poetry run uvicorn practice.main:app --host 0.0.0.0 --port 8000 & poetry run streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"]
