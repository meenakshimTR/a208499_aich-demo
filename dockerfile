FROM public.ecr.aws/docker/library/python:3.9

# Set the working directory to /app  
WORKDIR /app

COPY /src/ /app

# run pip upgrade command
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt  
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container  
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]