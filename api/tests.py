import uuid
import json
from django.test import TestCase, Client
from .models import Account, Destination
from .schemas import AccountSchema, AccountResponseSchema, DestinationSchema, DestinationResponseSchema

class APITestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_account(self):
        # Define the data for creating an account
        account_data = {
            "email": "test@example.com",
            "account_id": str(uuid.uuid4()),
            "account_name": "Test Account",
            "app_secret_token": str(uuid.uuid4()),
            "website": "https://example.com"
        }

        # Make a POST request to create an account
        response = self.client.post('/api/v1/accounts/', data=json.dumps(account_data), content_type='application/json')

        # Check if the account was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.json())
        self.assertEqual(response.json()['email'], account_data['email'])

        # Verify that the account exists in the database
        self.assertTrue(Account.objects.filter(email=account_data['email']).exists())

    def test_get_account(self):
        # Create a test account
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token=uuid.uuid4(), website="https://example.com")

        # Make a GET request to retrieve the account
        response = self.client.get(f'/api/v1/accounts/{test_account.account_id}')

        # Check if the account details are returned correctly
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.json())
        self.assertEqual(response.json()['email'], test_account.email)

    def test_update_account(self):
        # Create a test account
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token=uuid.uuid4(), website="https://example.com")

        # Define the data for updating the account
        updated_data = {
            "email": "updated@example.com",
            "account_name": "Updated Account",
            "website": "https://updated.com"
        }

        # Make a PUT request to update the account
        response = self.client.put(f'/api/v1/accounts/{test_account.account_id}', data=json.dumps(updated_data), content_type='application/json')

        # Check if the account was updated successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.json())
        self.assertEqual(response.json()['email'], updated_data['email'])

        # Verify that the account details are updated in the database
        updated_account = Account.objects.get(account_id=test_account.account_id)
        self.assertEqual(updated_account.email, updated_data['email'])
        self.assertEqual(updated_account.account_name, updated_data['account_name'])
        self.assertEqual(updated_account.website, updated_data['website'])

    def test_delete_account(self):
        # Create a test account
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token=uuid.uuid4(), website="https://example.com")

        # Make a DELETE request to delete the account
        response = self.client.delete(f'/api/v1/accounts/{test_account.account_id}')

        # Check if the account was deleted successfully
        self.assertEqual(response.status_code, 204)

        # Verify that the account is no longer present in the database
        self.assertFalse(Account.objects.filter(account_id=test_account.account_id).exists())

    def test_create_destination(self):
        # Create a test account
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token=uuid.uuid4(), website="https://example.com")

        # Define the data for creating a destination
        destination_data = {
            "url": "https://example.com/destination",
            "http_method": "GET",
            "headers": {"Content-Type": "application/json"}
        }

        # Make a POST request to create a destination
        response = self.client.post(f'/api/v1/accounts/{test_account.account_id}/destinations/', data=json.dumps(destination_data), content_type='application/json')

        # Check if the destination was created successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn('url', response.json())
        self.assertEqual(response.json()['url'], destination_data['url'])

        # Verify that the destination exists in the database
        self.assertTrue(Destination.objects.filter(url=destination_data['url']).exists())

    def test_list_destinations(self):
        # Create a test account
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token=uuid.uuid4(), website="https://example.com")

        # Create test destinations for the account
        destination1 = Destination.objects.create(account=test_account, url="https://example.com/destination1", http_method="GET", headers={"Content-Type": "application/json"})
        destination2 = Destination.objects.create(account=test_account, url="https://example.com/destination2", http_method="POST", headers={"Content-Type": "application/json"})

        # Make a GET request to retrieve the list of destinations
        response = self.client.get(f'/api/v1/accounts/{test_account.account_id}/destinations/')

        # Check if the list of destinations is returned correctly
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 2)  # Assuming we created two destinations

        # Verify the details of the returned destinations
        self.assertEqual(response.json()[0]['url'], destination1.url)
        self.assertEqual(response.json()[1]['url'], destination2.url)

    def test_handle_incoming_data(self):
        test_account = Account.objects.create(email="test@example.com", account_id=uuid.uuid4(), account_name="Test Account", app_secret_token="test_token", website="https://example.com")
        destination = Destination.objects.create(account=test_account, url="https://httpbin.org/post", http_method="POST", headers={"Content-Type": "application/json"})
        incoming_data = {
            "key1": "value1",
            "key2": "value2"
        }
        response = self.client.post('/api/v1/server/incoming_data', data=json.dumps(incoming_data), content_type='application/json', HTTP_CL_X_TOKEN='test_token')
        self.assertEqual(response.status_code, 200)
        self.assertIn('status', response.json())
        self.assertEqual(response.json()['status'], "success")
        self.assertIsInstance(response.json()['responses'], list)
        self.assertEqual(response.json()['responses'][0]['url'], destination.url)
        self.assertEqual(response.json()['responses'][0]['status_code'], 200)