# Use official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn pandas lunarcalendar pydantic

# Expose the FastAPI default port
EXPOSE 8000

# Run the FastAPI application
CMD ["uvicorn", "bazi_calulate_fastapi:app", "--host", "0.0.0.0", "--port", "8000"]
