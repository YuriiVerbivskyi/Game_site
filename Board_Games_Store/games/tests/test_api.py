import pytest
from rest_framework import status
from games.models import Game
from django.contrib.auth.models import User

pytestmark = pytest.mark.django_db



class TestGameCRUD:
    URL_LIST = '/games/'


    def test_list_games_success(self, api_client, test_game):
        response = api_client.get(self.URL_LIST)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Test Game Title'


    def test_retrieve_game_success(self, api_client, test_game):
        url = f'/games/{test_game.id}/'
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'Test Game Title'


    def test_retrieve_game_not_found(self, api_client):
        response = api_client.get('/games/9999/')
        assert response.status_code == status.HTTP_404_NOT_FOUND


    def test_create_game_unauthenticated(self, api_client, test_publisher):
        data = {
            'name': 'New Game', 'price': 500, 'publisher': test_publisher.id, 'genre': 'Puzzle',
            'players': '1-2', 'duration': '30', 'description': 'desc'
        }
        response = api_client.post(self.URL_LIST, data=data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_game_authenticated_success(self, auth_client, test_publisher):
        data = {
            'name': 'New Game 2', 'price': 500, 'publisher': test_publisher.id, 'genre': 'Puzzle',
            'players': '1-2', 'duration': '30', 'description': 'desc'
        }
        response = auth_client.post(self.URL_LIST, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert Game.objects.count() == 2

    def test_create_game_invalid_data(self, auth_client, test_publisher):
        data = {
            'name': 'Missing Price',
            'publisher': test_publisher.id,
            'description': 'Test desc',
            'genre': 'Strategy',
            'players': '2-4',
            'duration': '60',
        }
        response = auth_client.post(self.URL_LIST, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'price' in response.data


    def test_delete_game_unauthenticated(self, api_client, test_game):
        url = f'/games/{test_game.id}/'
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert Game.objects.count() == 1

    def test_delete_game_authenticated_success(self, auth_client, test_game):
        url = f'/games/{test_game.id}/'
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Game.objects.count() == 0


class TestAuthentication:
    URL_REGISTER = '/auth/register/'
    URL_LOGIN = '/auth/token/'


    def test_register_success(self, api_client, user_password):
        data = {
            'username': 'user',
            'email': 'new@gmail.com',
            'password': user_password,
            'password_check': user_password
        }
        response = api_client.post(self.URL_REGISTER, data=data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='user').exists()

    def test_register_password_mismatch(self, api_client):
        data = {
            'username': 'user',
            'email': 'new@gmail.com',
            'password': 'password1',
            'password_check': 'password2'
        }
        response = api_client.post(self.URL_REGISTER, data=data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password_check' in response.data


    def test_login_success(self, api_client, simple_user, user_password):
        data = {'username': simple_user.username, 'password': user_password}
        response = api_client.post(self.URL_LOGIN, data=data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['username'] == simple_user.username

    def test_login_invalid_password(self, api_client, simple_user):
        data = {'username': simple_user.username, 'password': 'wrong_password'}
        response = api_client.post(self.URL_LOGIN, data=data, format='json')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED