FROM python:3.12-slim
RUN pip install --no-cache-dir pytest
RUN useradd --create-home runner
USER runner
WORKDIR /work
ENV PYTHONDONTWRITEBYTECODE=1