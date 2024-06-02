import requests
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.api_data import ApiDataModel

def display_record_count(session):
    """
    Function to display the count of records in the 'ApiDataModel' table.

    Parameters:
        session: SQLAlchemy session object used to interact with the database.

    Returns:
        None
    """
    try:
        record_count = session.query(ApiDataModel).count()
        print(f"Number of records in the table: {record_count}")
    except SQLAlchemyError as e:
        print(f"Error: {e}")

def display_first_five_records(session):
    """
    Function to display the details of the first five records in the 'ApiDataModel' table.

    Parameters:
        session: SQLAlchemy session object used to interact with the database.

    Returns:
        None
    """
    try:
        # Fetching the first 5 records from the table
        records = session.query(ApiDataModel).limit(5).all()

        # Printing the details of each record
        print("\nFirst 5 records in the table ordered by ID number:")
        for record in records:
            print(f"ID: {record.id}, Name: {record.name}, Timestamp: {record.timestamp}, Value: {record.value}, "
                  f"Weekday: {record.weekday}, Days till Christmas: {record.days_till_christmas}, "
                  f"Days till Halloween: {record.days_till_halloween}")

    except SQLAlchemyError as e:
        print(f"Error: {e}")

def check_json_data(json_data, session):
    """
    Function to check the validity of JSON data for inserting into the 'ApiDataModel' table.
    
    Parameters:
        json_data: A dictionary containing the data to be checked.
        session: SQLAlchemy session object used to interact with the database.
    
    Returns:
        bool: True if the data is valid and can be inserted, False otherwise.
    """
    
    # List of required fields that must be present in the JSON data

    required_fields = ["id", "name", "timestamp", "value"]
    
    # Dictionary specifying the expected data type for each field

    field_types = {
        "id": int,
        "name": str,
        "timestamp": str,
        "value": int
    }
    
    # Lists to keep track of missing and invalid fields

    missing_fields = []
    invalid_fields = []

    try:
        # Loop through each required field to check its presence and validity

        for field in required_fields:
            if field not in json_data:
                # Add to missing fields if the field is not present
                missing_fields.append(field)
            elif json_data[field] is None:
                # Add to invalid fields if the field is None
                invalid_fields.append(field)
            elif not isinstance(json_data[field], field_types[field]):
                # Add to invalid fields if the field has an incorrect type
                invalid_fields.append(field)

        try:
            # Check if id is already present in the table
            if "id" in json_data:
                id_value = int(json_data["id"]) # Ensure 'id' is an integer
                existing_record = session.query(ApiDataModel).filter_by(id=id_value).first()
                if existing_record:
                    # Print error message and return False if 'id' already exists
                    print(f"Error: ID {id_value} already present in table. Record not inserted.")
                    return False
        except ValueError:
            # Handle the case where 'id' is not a valid integer
            print("Error: ID must be an integer.")
            return False

    except Exception as e:
        # Catch any other exceptions and print an error message
        print("An error occurred while checking JSON data:", e)
        return False    
    
    # Check for any missing fields and print an error message if found
    if missing_fields:
        print("Error: Missing values for fields:", ", ".join(missing_fields))
        return False
    elif invalid_fields:
        # Check for any invalid fields and print an error message if found
        print("Error: Invalid values for fields:", ", ".join(invalid_fields))
        return False
    else:        
        # Return True if no issues are found with the JSON data
        return True



def fetch_and_insert_data(api_url, session):
    """
    Function to fetch data from an API, process it, and insert it into the 'ApiDataModel' table.

    Parameters:
        api_url (str): The URL of the API to fetch data from.
        session: SQLAlchemy session object used to interact with the database.

    Returns:
        None
    """
    
    try:
        # Fetch data from the API
        response = requests.get(api_url)
        response.raise_for_status() # Raise an HTTPError for bad responses
        json_data = response.json() # Parse JSON data
        print("\nOriginal JSON fetched from API:",json_data)

        # Check if all required fields have appropriate values
        if not check_json_data(json_data,session):
            # If any required fields are missing, exit the function
            exit()

        # Get the weekday from the timestamp and convert it to string
        timestamp = datetime.fromisoformat(json_data["timestamp"])
        weekday_name = timestamp.strftime("%A")  # Format to get the full weekday name

        # Calculate days till Christmas from the timestamp
        today = timestamp.date()
        christmas = datetime(today.year, 12, 25).date()
        if today > christmas:             
            # If today is after Christmas, calculate for the next year
            christmas = datetime(today.year + 1, 12, 25).date()
        days_till_christmas = (christmas - today).days

        # Calculate days till Halloween from the timestamp
        halloween = datetime(today.year, 10, 31).date()
        if today > halloween: 
            # If today is after Halloween, calculate for the next year
            halloween = datetime(today.year + 1, 10, 31).date()
        days_till_halloween = (halloween - today).days

        # Normalize the name string input by removing all whitespace characters and converting to lowercase
        normalized_name = json_data["name"].strip().lower().replace(" ", "")

        # Create a new record to insert into the database
        new_record = ApiDataModel(
            id=json_data['id'],
            name=normalized_name,
            timestamp=timestamp,
            value=json_data["value"] * 2, # "value" data transformed by multiplying by 2
            weekday=weekday_name,
            days_till_christmas=days_till_christmas,
            days_till_halloween=days_till_halloween
        )
        # Display the contents of new_record before inserting it to the database

        print("\nContents of record inserted in database:")
        print(f"ID: {new_record.id}")
        print(f"Name: {new_record.name}")
        print(f"Timestamp: {new_record.timestamp}")
        print(f"Value: {new_record.value}")
        print(f"Weekday: {new_record.weekday}")
        print(f"Days till Christmas: {new_record.days_till_christmas}")
        print(f"Days till Halloween: {new_record.days_till_halloween}")

        #Inserting the new record into the database
        session.add(new_record)
        session.commit()

        print("Data successfully fetched and stored")

    except requests.RequestException as e:
        # Handle errors that occur during the API request
        print(f"Error fetching data from API: {e}")

    except SQLAlchemyError as e:
        # Handle errors that occur during the database operations
        session.rollback()  # Rollback the transaction in case of error
        print(f"Database error: {e}")
