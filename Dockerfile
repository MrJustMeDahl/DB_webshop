FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install Python packages
RUN pip install --upgrade pip && pip install --no-cache-dir \
    streamlit==1.45.0 \
    st-pages==1.0.1 \
    redis==5.2.1 \
    mysql-connector-python==9.3.0 \
    pymongo==4.12.1 \
    lorem-text==3.0 \
    pandas==2.2.3
    
# Ensure streamlit is on PATH
ENV PATH="/usr/local/bin:$PATH"
ENV PYTHONPATH=/app
