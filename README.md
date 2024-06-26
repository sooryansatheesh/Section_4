# Soorya's Database Application /Section 4 -Coding Exercise

Welcome to Soorya's Database Application! This application fetches data from a mock API (https://mock-api-im8j.onrender.com/mock_api) and stores it in an SQLite database. You can interact with the database through a menu-driven interface.

## About the mock API

A mock API was created using Flask, which generates random data for each request through the /mock_api endpoint. The data generated by this endpoint includes an id (a random integer between 1 and 1000), a name (a string formatted as "Item" followed by a random integer between 1 and 100), a timestamp (the current date and time in ISO format), and a value (a random integer between 1 and 100). The Flask application was Dockerized by writing a Dockerfile to build an image, encapsulating the necessary environment and dependencies. This Docker image was then pushed to Docker Hub (Image name - sooryanarayan/mock_api:latest), making it publicly accessible. Finally, the Docker image was deployed on Render.com, a cloud platform that facilitates easy deployment and scaling of applications, thus enabling the mock API to be used for Section_4.

## Features

- Fetch new records from a mock API and insert them into the database.
- Handling edge cases effectively.
- Transformation of data fetched from the mock API
    - "name" is normalized by removing white spaces and converting all characters to lowercase
    - "timestamp" is converted from string to datetime format
    - "value" is multiplied by 2
    - Day of the week is identified from the timestamp and inserted as a new field "weekday"
    - The number of days from timestamp to Christmas is calculated and inserted as a new field "days_till_christmas"
    - The number of days from timestamp to Halloween is calculated and inserted as a new field "days_till_halloween"
- View the first 5 records in the database, ordered by ID.
- Persistent storage of database records using Docker volumes.

## Requirements

- Docker
- Docker Compose

## Project Structure
```css
Section_4/
├── docker-compose.yml
└── app/
    ├── Dockerfile
    ├── main.py
    ├── models/
    │   └── api_data.py
    ├── resources/
    │   └── api_data.py
    ├── api_data.db
    └── requirements.txt

```
## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/sooryansatheesh/section_4.git
cd section_4
```
### 2. Create requirements.txt
Ensure you have a requirements.txt file with the necessary dependencies. Here's an example:
```sh
SQLAlchemy==1.4.22

requests==2.25.1
```

### 3. Build and Run the Application with Docker Compose
Build and run the Docker container using Docker Compose:
```sh
docker-compose up --build -d
```
This command will build the Docker image and start the container in detached mode. The database file will be persisted in the ./app directory on your host machine.

### 4. Attach to the Running Container
To interact with the application, attach to the running container:

1. List the running containers to get the container ID or name:
```sh
docker ps
```
2. Attach to the container (replace <container_id_or_name> with your container's ID or name), then press enter to display the menu:
```sh
docker attach <container_id_or_name>
```
You will be presented with a menu:
```vbnet
Welcome to Soorya's Database
Number of records in the database: X

Menu Options:
1. Fetch a new record from the API and insert into the database
2. View the first 5 records in the table ordered by ID number
3. Exit

Enter your choice (1, 2, or 3):
```
- Choose 1 to fetch and insert new records.
- Choose 2 to view the first 5 records.
- Choose 3 to exit the program.

### 5. Persisting Data

The volume mount in the Docker Compose file ensures that your database file (`api_data.db`) is stored on your host machine, allowing data to persist across container restarts.

## Notes

- Make sure Docker and Docker Compose are installed and running on your system.
- Replace the path in the docker-compose.yml file with the appropriate path on your host machine if needed.
- Since the mock API is stored in the free tier of Render.com it would be idle and may require some time to wake up when accessed for the first time, while subsequent access will be fast.
- After running the `docker attach` command press the enter button a few times to display the menu.  

## Troubleshooting

- If the database is not persisting, ensure the volume is correctly mounted and the database path is correct.
