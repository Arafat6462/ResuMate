# 1. Base Image: Start from a lightweight, official Python image.
FROM python:3.11-slim-buster

# 2. Set Environment Variables:
#    - Prevents Python from writing .pyc files to disc.
#    - Prevents Python from buffering stdout and stderr.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Set Work Directory:
#    - Create and set the working directory inside the container.
WORKDIR /app

# 4. Install Dependencies:
#    - Copy the requirements file into the container.
#    - Install the Python dependencies. Using --no-cache-dir keeps the image smaller.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy Project Code:
#    - Copy the rest of our application's code from our local machine into the container.
COPY . .

# 6. Collect Static Files:
#    - Run the collectstatic command to gather all static files into STATIC_ROOT.
#    - This needs to be done before the application starts.
RUN python manage.py collectstatic --noinput

# 7. Expose Port:
#    - Inform Docker that the application inside the container will listen on port 8000.
EXPOSE 8000

# 8. Set Default Command for Production:
#    - Run database migrations and start Gunicorn as the production WSGI server.
CMD ["sh", "-c", "python manage.py migrate && gunicorn ResuMate_backend.wsgi:application --bind 0.0.0.0:$PORT"]
