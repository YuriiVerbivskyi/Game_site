import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from games.models import Publisher, Game


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture
def user_password():
    return 'Strong_Pa$$word123'


@pytest.fixture
def simple_user(user_password):
    user = User.objects.create_user(
        username='test',
        email='test@example.com',
        password=user_password
    )
    yield user


@pytest.fixture
def auth_client(api_client: APIClient, simple_user: User):
    refresh = RefreshToken.for_user(simple_user)
    access_token = str(refresh.access_token)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    yield api_client

    api_client.credentials()



@pytest.fixture
def test_publisher():
    return Publisher.objects.create(
        name='Test Publisher Inc.',
        country='UA',
        founded=2020
    )


@pytest.fixture
def test_game(test_publisher: Publisher):
    return Game.objects.create(
        name='Test Game Title',
        description='A unique description.',
        price=1000,
        publisher=test_publisher,
        genre='Strategy',
        players='2-4',
        duration='60'
    )