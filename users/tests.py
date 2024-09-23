import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from ShopZoneConfig.conftest import *


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_signup(api_client):
    url = reverse('user_mgt:signup')
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "PAQe1234s!ord",
        "user_type": "user"
    }
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert response.data["data"]["username"] == "newuser"
    assert response.data["message"] == "Registration successful"


@pytest.mark.django_db
def test_signup_existing_user(api_client, create_user):
    url = reverse('user_mgt:signup')
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "QwXERT1234!@",
        "user_type": "user"
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert response.data["success"] == False


@pytest.mark.django_db
def test_login(api_client, create_user):
    url = reverse('user_mgt:login')
    data = {
        'password' : 'AS240183U!@!#@', 
        'email' : 'testuser@example.com',
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert response.data["message"] == "Login successful"
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_login_invalid_credentials(api_client):
    url = reverse('user_mgt:login')
    data = {
        'password' : 'password', 
        'email' : 'testuser@example.com',
    }
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert response.data["message"] == "Invalid login credentials"


@pytest.mark.django_db
def test_user_viewset_authenticated_user(api_client, get_access_token):
    access_token = get_access_token
    user_url = reverse('user_mgt:users-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(user_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_viewset_patch_user(api_client, create_user, get_access_token):
    access_token = get_access_token
    user_id = create_user.id
    patch_url = reverse('user_mgt:users-detail', kwargs={'pk': user_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    patch_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com'
    }
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 200
    assert response.data['username'] == 'updateduser'
    assert response.data['email'] == 'updateduser@example.com'


@pytest.mark.django_db
def test_user_viewset_authenticated_user(api_client, create_user, get_access_token):
    login_url = reverse('user_mgt:login')
    login_data = {
        'password' : 'AS240183U!@!#@', 
        'email' : 'testuser@example.com',
    }
    login_response = api_client.post(login_url, login_data)
    access_token = login_response.data['access']
    user_url = reverse('user_mgt:users-list')
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.get(user_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_viewset_unauthenticated(api_client):
    user_url = reverse('user_mgt:users-list')
    response = api_client.get(user_url)
    assert response.status_code == 401

@pytest.mark.django_db
def test_user_viewset_patch_user(api_client, create_user, get_access_token):
    login_url = reverse('user_mgt:login')
    login_data = {
        'password' : 'AS240183U!@!#@', 
        'email' : 'testuser@example.com',
    }
    login_response = api_client.post(login_url, login_data)
    access_token = login_response.data['access']
    user_id = create_user.id
    patch_url = reverse('user_mgt:users-detail', kwargs={'pk': user_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    patch_data = {
        'username': 'updateduser',
        'email': 'updateduser@example.com'
    }
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 200
    assert response.data['username'] == 'updateduser'
    assert response.data['email'] == 'updateduser@example.com'


@pytest.mark.django_db
def test_user_viewset_delete_user(api_client, create_user, get_access_token):
    access_token = get_access_token
    user_id = create_user.id
    delete_url = reverse('user_mgt:users-detail', kwargs={'pk': user_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 204

