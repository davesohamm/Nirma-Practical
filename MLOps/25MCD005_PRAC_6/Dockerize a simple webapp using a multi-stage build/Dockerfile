# -------- Stage 1: Build dependencies --------
FROM python:3.13-slim AS builder

WORKDIR /build

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements.txt


# -------- Stage 2: Final image --------
FROM python:3.13-slim

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /build/wheels /wheels


RUN pip install --no-cache-dir /wheels/*

COPY . .

EXPOSE 8000

# Run app
CMD ["python", "app.py"]