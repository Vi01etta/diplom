import pytest
from django.urls import reverse
from rest_framework.test import APIRequestFactory, force_authenticate
from backend.models import User, Shop
from backend.views import PartnerState, PartnerUpdate

create_data = {'email': 'qwerty@mail.com',
               'password': 'hdthggshxth',
               'first_name': 'Vladimir',
               'last_name': 'Victorovich',
               'company': 'Gazprom',
               'position': 'Manager',
               }

@pytest.fixture()
def client():
    return APIRequestFactory()



def urls(name):
    url = reverse("backend:" + name)
    return url


@pytest.mark.django_db
def test_shops(client):
    response = client.get(urls(name='shops'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_account(client):
    response = client.post(urls(name='user-register'), create_data)
    assert response.status_code == 200
    assert response.json().get('Status') is True

    user = User.objects.get(email=create_data['email'])
    user.is_active = True
    user.save()

    response = client.post(urls(name='user-login'),
                           create_data)
    assert response.status_code == 200
    assert response.json().get('Status') is True


@pytest.mark.django_db
def test_partner_update(client):
    user = User.objects.create_user(email=create_data['email'],
                                    password=create_data['password'])
    user.is_active = True
    user.type = 'shop'
    user.save()

    force_authenticate(user)
    view = PartnerUpdate.as_view()

    price_info = 'https://github.com/Vi01etta/diplom/blob/master/data/shop1.yaml'
    request = client.post(urls(name='partner-update'), url=price_info)
    response = view(request)
    assert response.status_code == 201


@pytest.mark.django_db
def test_partner_state(client):
    user = User.objects.create_user(email=create_data['email'],
                                    password=create_data['password'], first_name=create_data['first_name'])
    user.is_active = True
    user.type = 'shop'
    user.save()

    force_authenticate(user)
    view = PartnerState.as_view()

    shop = Shop.objects.create(name='DNS', user=user)
    shop.state = 'True'
    shop.save()

    request = client.post(urls(name='partner-state'), data={'shop': shop})
    response = view(request)
    assert response.status_code == 201
