# ============================================================
# Dockerfile — Result-Check Flask Application
# Multi-stage approach: slim base for small final image
# ============================================================

# --- Base image ---
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Create a non-root user for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set working directory
WORKDIR /app

# Copy and install dependencies FIRST (for Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app.py .
COPY results.py .
COPY templates/ templates/
COPY static/ static/

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app
USER appuser

# Expose application port
EXPOSE 5000

# Health check — Docker will mark the container unhealthy if this fails
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"

# Start the Flask app with Gunicorn (production-grade WSGI server)
# Falls back to Flask dev server if gunicorn is not installed
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
