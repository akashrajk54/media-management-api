## media-management-api
A Django-based REST API service for video file management, allowing users to upload, trim, and merge video files. The service supports configurable size and duration limits, video link sharing with time-based expiry, and includes unit and end-to-end testing. Built with SQLite for easy setup and extensibility.


## Setup

   1. Clone the repository:
       git clone https://github.com/akashrajk54/media-management-api.git

   2. Navigate to the project directory:
       cd media-management-api

   3. Create a virtual environment (optional but recommended):
       python -m venv venv

   4. Activate the virtual environment:
      a). Windows:
          venv\Scripts\activate
      b). Linux/macOS:
          source venv/bin/activate

   5. Install dependencies:
      pip install -r requirements.txt

   6. Set up environment variables:
        Download .env file from shared email and keep it within **media-management-api** 

       ### During production 
            
            Debug = False
        
            ALLOWED_HOSTS = insted of ['*'], please add specific frontend url, so that request from anyother will be rejected.

   7. Run migrations to create the database schema:
      
      python manage.py makemigrations
      
      python manage.py migrate

   8. Create a superuser (admin) account:
      
      python manage.py createsuperuser

   9. Run the development server:
      
      python manage.py runserver
      
      (by default it will use 8000 port)

   10. To run test cases:
       
       cd backends_engine
       
        pytest test.py


## Code Quality

    The code adheres to SOLID principles and is designed with best practices for maintainability and scalability.
    Logging is implemented for debugging, error tracking, and informational purposes.

## Contributing

    Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


