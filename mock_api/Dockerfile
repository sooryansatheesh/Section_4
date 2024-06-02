# base image
FROM python:3.10


# port where the app will run
EXPOSE 5001


# move into the folder where the Flask app will go
WORKDIR /app

# Copy just the requirements file
COPY requirements.txt .

RUN pip install -r requirements.txt


# copy from your system into the images' file system
# first dot: copy everything in the current folder (local)
# second dot: to the current folder of the image (/app as we specified above)
COPY . .


# commands that should run when the image starts a container - replace with your file name
CMD ["flask", "--app", "mock_api.py", "run", "--host", "0.0.0.0", "--port", "5001"]