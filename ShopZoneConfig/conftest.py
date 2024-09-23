import pytest
from users.models import User
from django.urls import reverse

@pytest.fixture
def create_user(db):
    return User.objects.create_user(
        username='testuser', 
        password='AS240183U!@!#@', 
        email='testuser@example.com',
        user_type='user'
    )


@pytest.fixture
def create_user_2(db):
    return User.objects.create_user(
        username='user2', 
        password='L>k3#$%1#@', 
        email='testuser2@example.com',
        user_type='user'
    )


@pytest.fixture
def create_admin_user(db):
    return User.objects.create_superuser(
        username='admin', 
        password='akka@#$#FR12',
        email='admin@example.com',
        user_type='admin'
    )


@pytest.fixture
def get_access_token(api_client, create_user):
    login_url = reverse('user_mgt:login')
    login_data = {
        'password': 'AS240183U!@!#@', 
        'email': 'testuser@example.com',
    }
    login_response = api_client.post(login_url, login_data)
    assert login_response.status_code == 200
    return login_response.data['access']


@pytest.fixture
def get_access_token_2(api_client, create_user_2):
    login_url = reverse('user_mgt:login')
    login_data = {
        'password': 'L>k3#$%1#@',
        'email': 'testuser2@example.com',
    }
    login_response = api_client.post(login_url, login_data)
    assert login_response.status_code == 200
    return login_response.data['access']


@pytest.fixture
def get_admin_access_token(api_client, create_admin_user):
    login_url = reverse('user_mgt:login')
    login_data = {
        'password': 'akka@#$#FR12',
        'email': 'admin@example.com',
    }
    login_response = api_client.post(login_url, login_data)
    assert login_response.status_code == 200
    return login_response.data['access']


