
from sqlalchemy import create_engine
from sqlalchemy.orm import  sessionmaker
from models.api_data import Base
from resources.api_data import display_first_five_records,display_record_count,fetch_and_insert_data

# Database setup
DATABASE_URL = "sqlite:///api_data.db" # Define the database URL
engine = create_engine(DATABASE_URL) # Create a SQLAlchemy engine

# Create the table
# Uncomment the following line to drop all tables (use with caution)
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine) # Create tables based on the Base metadata

# Create a configured "Session" class
Session = sessionmaker(bind=engine)


def main_menu():
    """
    Main menu function to interact with the database.
    
    This function provides options to fetch new records from the API, view the first five records,
    and exit the program. It interacts with the database using SQLAlchemy sessions.
    """
    
    session = Session()
    
    while True:
        # Display the welcome message and the current record count
        print("\nWelcome to Soorya's Database\n===============================")
        
        display_record_count(session)
        # Display menu options
        print("\nMenu Options:")
        print("1. Fetch a new record from the API and insert into the database")
        print("2. View the first 5 records in the table ordered by ID number")
        print("3. Exit")

        # Get the user's choice
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            # Fetch and insert a new record from the API
            fetch_and_insert_data("https://mock-api-im8j.onrender.com/mock_api", session)
        elif choice == '2':
            # Display the first five records in the table order by ID number
            display_first_five_records(session)
        elif choice == '3':
            # Exit the program
            print("Exiting the program.")
            break
        else:
            # Handle invalid menu choices
            print("Invalid choice. Please select 1, 2, or 3.")
    
    session.close() # Close the session when done

if __name__ == "__main__":
    main_menu() # Run the main menu function if this script is executed