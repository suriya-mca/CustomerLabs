# Data Pusher Django Application

## Overview

This Django application receives data from an account and sends it to multiple destinations based on webhook URLs. The received data is stored in the database before being forwarded.

## Setup

1. Clone the repository and navigate to the project directory.

    ```bash
    git clone <repository_url>
    cd data_pusher
    ```

2. Create and activate a virtual environment.

    ```bash
    python -m venv venv
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

## API Endpoints

### Account Endpoints

- **Create Account**: `POST /api/accounts/`
- **Retrieve Account**: `GET /api/accounts/{account_id}/`
- **Update Account**: `PUT /api/accounts/{account_id}/`
- **Delete Account**: `DELETE /api/accounts/{account_id}/`

### Destination Endpoints

- **Create Destination**: `POST /api/destinations/`
- **Retrieve Destination**: `GET /api/destinations/{destination_id}/`
- **Update Destination**: `PUT /api/destinations/{destination_id}/`
- **Delete Destination**: `DELETE /api/destinations/{destination_id}/`

### Incoming Data Endpoint

- **Receive Data**: `POST /api/server/incoming_data`