import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from .models import *
from ShopZoneConfig.conftest import *


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_category(db):
    category = Category.objects.create(name="Stationaries", description="Stationaries")
    return category


@pytest.fixture
def create_store(db, create_user):
    store = Store.objects.create(name="Mannuel Store", owner=create_user,
        description="Mannuel Store", address="Ikeja, Lagos")
    return store


@pytest.fixture
def create_product(db, create_store, create_category):
    product = Product.objects.create(
        name="Test Product", 
        store=create_store, 
        category=create_category,
        price=100.00
    )
    return product


@pytest.mark.django_db
def test_create_category(api_client, get_admin_access_token):
    # only admins can create categories
    access_token = get_admin_access_token
    url = reverse('product_mgt:categories-list')
    data = {
        "name" : "Electronics",
        "description" : "Electronics gadgets",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.post(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_category(api_client, create_category, get_admin_access_token):
    # only admins can update categories
    access_token = get_admin_access_token
    data = {
        "name" : "Electronics",
        "description" : "Electronics gadgets",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_category.id
    patch_url = reverse('product_mgt:categories-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'New Stationaries'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 200
    assert response.data['name'] == 'New Stationaries'


@pytest.mark.django_db
def test_delete_category(api_client, create_category, get_admin_access_token):
    # only admins can delete categories
    access_token = get_admin_access_token
    category_id = create_category.id
    delete_url = reverse('user_mgt:users-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_patch_category_user(api_client, create_category, get_access_token):
    # users can't update categories
    access_token = get_access_token
    data = {
        "name" : "Electronics",
        "description" : "Electronics gadgets",
    }
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_category.id
    patch_url = reverse('product_mgt:categories-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'New Stationaries'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_category_user(api_client, create_category, get_access_token):
    # users can't delete categories
    access_token = get_access_token
    category_id = create_category.id
    delete_url = reverse('product_mgt:categories-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_store_create(api_client, create_user, get_access_token):
    access_token = get_access_token
    url = reverse('product_mgt:stores-list')
    data = {
        "owner" : create_user.id,
        "name" : "New Store",
        "description" : "New Store",
        "address" : "V.I, Lagos"
    }
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.post(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_store(api_client, create_store, get_access_token):
    access_token = get_access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_store.id
    patch_url = reverse('product_mgt:stores-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'Updated Store'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_store(api_client, create_store, get_access_token):
    access_token = get_access_token
    category_id = create_store.id
    delete_url = reverse('product_mgt:stores-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_patch_other_store(api_client, create_store, get_access_token_2):
    # a user, can't update another user's store
    access_token = get_access_token_2
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_store.id
    patch_url = reverse('product_mgt:stores-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'Updated Store'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_other_store(api_client, create_store, get_access_token_2):
    # a user, can't delete another user's store
    access_token = get_access_token_2
    category_id = create_store.id
    delete_url = reverse('product_mgt:stores-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_product_create(api_client, create_user, create_store, create_category, get_access_token):
    access_token = get_access_token
    url = reverse('product_mgt:products-list')
    data = {
        "name": "New Product",
        "price": 200.00,
        "store": create_store.id,
        "category": create_category.id
    }
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.post(url, data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_product(api_client, create_product, get_access_token):
    access_token = get_access_token
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_product.id
    patch_url = reverse('product_mgt:products-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'Updated Store'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_product(api_client, create_product, get_access_token):
    access_token = get_access_token
    category_id = create_product.id
    delete_url = reverse('product_mgt:products-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 204


@pytest.mark.django_db
def test_patch_other_product(api_client, create_product, get_access_token_2):
    # a user, can't update another user's product
    access_token = get_access_token_2
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    category_id = create_product.id
    patch_url = reverse('product_mgt:products-detail', kwargs={'pk': category_id})
    patch_data = {'name': 'Updated Store'}
    response = api_client.patch(patch_url, patch_data, format='json')
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_other_product(api_client, create_product, get_access_token_2):
    # a user, can't delete another user's product
    access_token = get_access_token_2
    category_id = create_product.id
    delete_url = reverse('product_mgt:products-detail', kwargs={'pk': category_id})
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    response = api_client.delete(delete_url)
    assert response.status_code == 403

