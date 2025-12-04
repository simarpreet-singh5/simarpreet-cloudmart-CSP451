FROM python:3.11-slim

WORKDIR /app

# Install backend dependencies
COPY applications/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY applications/backend/app/ app/

# Copy frontend static files into /app/static
COPY applications/frontend/src/ static/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
