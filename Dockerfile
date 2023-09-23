# Using an official python base image: https://hub.docker.com/_/python

# STEP 1. Install a python base image (using alpine for apk)
FROM python:3.9-alpine

# STEP 2. Set working directory to /app so we can execute commands in it
WORKDIR /app

# STEP 3. Copy all app code into /app
COPY . .

# STEP 4. Install required dependencies (fancy due to error with psycopg2)
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev libffi-dev
RUN pip install -r requirements.txt

# STEP 5. Decclare env variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# STEP 6. Expose the port that Flask is running on
EXPOSE 8000

# STEP 7: Run Flask!
CMD ["python3", "app.py"]
