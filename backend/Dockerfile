FROM python:3.10-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip wheel setuptools

COPY --from=builder /install /usr/local

COPY src/common/ ./src/common/
COPY src/prediction/ ./src/prediction/
COPY backend/ ./backend/

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
