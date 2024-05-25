from ninja import Router

import requests
import uuid
from django.shortcuts import get_object_or_404
from typing import List

from .models import Account, Destination
from .schema import AccountSchema, AccountResponseSchema, DestinationSchema, DestinationResponseSchema


router = Router()

@router.post("/accounts/", response=AccountResponseSchema)
def create_account(request, account: AccountSchema):
    new_account = Account.objects.create(**account.dict())
    return new_account

@router.get("/accounts/{account_id}", response=AccountResponseSchema)
def get_account(request, account_id: uuid.UUID):
    account = get_object_or_404(Account, account_id=account_id)
    return account

@router.put("/accounts/{account_id}", response=AccountResponseSchema)
def update_account(request, account_id: uuid.UUID, account: AccountSchema):
    account_obj = get_object_or_404(Account, account_id=account_id)
    for attr, value in account.dict().items():
        setattr(account_obj, attr, value)
    account_obj.save()
    return account_obj

@router.delete("/accounts/{account_id}", response={204: None})
def delete_account(request, account_id: uuid.UUID):
    account = get_object_or_404(Account, account_id=account_id)
    account.delete()
    return 204

@router.post("/accounts/{account_id}/destinations/", response=DestinationResponseSchema)
def create_destination(request, account_id: uuid.UUID, destination: DestinationSchema):
    account = get_object_or_404(Account, account_id=account_id)
    new_destination = Destination.objects.create(account=account, **destination.dict())
    return new_destination

@router.get("/accounts/{account_id}/destinations/", response=List[DestinationResponseSchema])
def list_destinations(request, account_id: uuid.UUID):
    account = get_object_or_404(Account, account_id=account_id)
    return account.destinations.all()

@router.post("/server/incoming_data", response=dict)
def handle_incoming_data(request, data: dict):
    token = request.headers.get("CL-X-TOKEN")
    if not token:
        return {"error": "Un Authenticate"}

    account = get_object_or_404(Account, app_secret_token=token)
    destinations = account.destinations.all()

    responses = []
    for destination in destinations:
        headers = destination.headers
        url = destination.url
        method = destination.http_method
        if method == "GET":
            response = requests.get(url, headers=headers, params=data)
        else:
            response = requests.request(method, url, headers=headers, json=data)
        responses.append({"url": url, "status_code": response.status_code, "response": response.text})

    return {"status": "success", "responses": responses}