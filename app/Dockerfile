# base image
FROM python:3.10


# move into the folder where the app will go
WORKDIR /app

# Copy just the requirements file
COPY requirements.txt .

RUN pip install -r requirements.txt


# copy from your system into the images' file system
# first dot: copy everything in the current folder (local)
# second dot: to the current folder of the image (/app as we specified above)
COPY . /app/

# commands that should run when the image starts a container 
CMD ["python", "app.py"]