# Use the latest Python base image (3.11-slim)
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install essential build dependencies and tzdata for timezone configuration
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev curl tzdata && \
    rm -rf /var/lib/apt/lists/*

# Set the timezone to IST (Asia/Kolkata)
ENV TZ=Asia/Kolkata

# Ensure that the timezone setting takes effect
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy only the requirements file to leverage Docker's caching
COPY requirements.txt .

# Install Python dependencies with suppressed root warning
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Remove unnecessary build dependencies to reduce image size
RUN apt-get remove -y gcc libpq-dev && apt-get autoremove -y && apt-get clean

# Copy the rest of the application code into the container
COPY --chown=nonrootuser:nonrootuser . .

# Add a non-root user and switch to it
RUN useradd -m nonrootuser
USER nonrootuser

# Expose the application port (e.g., 8080)
EXPOSE 8080

# Set environment variables (can be overridden at runtime)
ENV HOST=0.0.0.0
ENV PORT=8080
ENV DEBUG=False
ENV THREADS=5

# Run the application with Waitress using the specified host, port, and thread count
CMD ["python3", "run.py"]
