# standard python image
FROM python:3.9

# Set working directory
WORKDIR /code

# Copy requirements file (we use the original one, or a specific one if needed)
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application
COPY . /code

# Create a directory for file uploads if it doesn't exist and set permissions
RUN mkdir -p /code/static/uploads && chmod 777 /code/static/uploads

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the application using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "main:app"]
