# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Add app directory to Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements_lite.txt .

# Install Python dependencies (lite version for memory optimization)
RUN pip install --no-cache-dir -r requirements_lite.txt

# Copy the application
COPY . .

# Debug: Check what was copied
RUN echo "=== APP DIRECTORY ===" && ls -la /app/
RUN echo "=== MODULES DIRECTORY ===" && ls -la /app/modules/
RUN echo "=== DESIGN_EXCEL FILE ===" && ls -la /app/modules/design_excel.py
RUN echo "=== PYTHON PATH ===" && python -c "import sys; print('Python path:', sys.path)"

# Create necessary directories
RUN mkdir -p vectorestores chroma_db_document_open_source Results

# Expose Streamlit port
EXPOSE 8501

# Set environment variables
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Memory optimization
ENV PYTHONUNBUFFERED=1
ENV MALLOC_ARENA_MAX=2

# Suppress warnings
ENV PYTHONWARNINGS="ignore::UserWarning,ignore::DeprecationWarning"

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "Rhizon.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
