FROM python:3.12-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY .ssl/cert_IRET-SSL-TrsutCA.crt /etc/ssl/certs/IRET-SSL-TrsutCA.crt

# Copy the application into the container.
COPY . /app

# Set the environment variables.
ENV UV_PROJECT_ENVIRONMENT='/usr/local/'
ENV UV_SYSTEM_PYTHON=1
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/IRET-SSL-TrsutCA.crt
ENV CURL_CA_BUNDLE=/etc/ssl/certs/IRET-SSL-TrsutCA.crt
ENV SSL_CERT_FILE=/etc/ssl/certs/IRET-SSL-TrsutCA.crt
ENV UV_HTTP_TIMEOUT=120

# Install the application dependencies.
WORKDIR /app

# Install the application dependencies.
RUN uv export --frozen --format requirements-txt > requirements.txt && \
uv pip install -r requirements.txt;

# Run the application.
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port=8000"]