# Data Pusher Django Application

## Overview

This Django application receives data from an account and sends it to multiple destinations based on webhook URLs. The received data is stored in the database before being forwarded.

## Setup by cloning the repo

1. Clone the repository and navigate to the project directory.

    ```bash
    git clone <repository_url>
    cd CustomerLabs
    ```

2. Create and activate a virtual environment.

    ```bash
    python -m venv env
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies.

    ```bash
    pip install -r requirements.txt
    ```

4. Apply migrations.

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Run the development server.

    ```bash
    python manage.py runserver
    ```

## Setup using docker

1. Run the following commands in a terminal:

    ```bash
    docker compose up
    ```
## Swagger UI

Now go to http://127.0.0.1:8000/api/docs

## API Endpoints

### Account Endpoints

- **Create Account**: `POST /api/v1/accounts/`
- **Retrieve Account**: `GET /api/v1/accounts/{account_id}/`
- **Update Account**: `PUT /api/v1/accounts/{account_id}/`
- **Delete Account**: `DELETE /api/v1/accounts/{account_id}/`

### Destination Endpoints

- **Create Destination**: `POST /api/v1/destinations/`
- **Retrieve Destination**: `GET /api/v1/destinations/{destination_id}/`

### Incoming Data Endpoint

- **Receive Data**: `POST /api/v1/server/incoming_data`
