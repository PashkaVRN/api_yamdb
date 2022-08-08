from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def create_users_api(admin_client):
    data = {
        'username': 'TestUser',
        'role': 'user',
        'email': 'testuser@yamdb.fake'
    }
    admin_client.post('/api/v1/users/', data=data)
    user = get_user_model().objects.get(username=data['username'])
    data = {
        'first_name': 'ModerFirstName',
        'last_name': 'ModerLastNAme',
        'username': 'TestModer',
        'bio': 'About me mafa yo',
        'role': 'moderator',
        'email': 'testmoder@yamdb.fake'
    }
    admin_client.post('/api/v1/users/', data=data)
    moderator = get_user_model().objects.get(username=data['username'])
    return user, moderator


def auth_client(user):
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client


def create_categories(admin_client):
    data1 = {
        'name': 'Фильм',
        'slug': 'films'
    }
    admin_client.post('/api/v1/categories/', data=data1)
    data2 = {
        'name': 'Книги',
        'slug': 'books'
    }
    admin_client.post('/api/v1/categories/', data=data2)
    return [data1, data2]


def create_genre(admin_client):
    result = []
    data = {'name': 'Ужасы', 'slug': 'horror'}
    result.append(data)
    admin_client.post('/api/v1/genres/', data=data)
    data = {'name': 'Комедия', 'slug': 'comedy'}
    result.append(data)
    admin_client.post('/api/v1/genres/', data=data)
    data = {'name': 'Драма', 'slug': 'drama'}
    result.append(data)
    admin_client.post('/api/v1/genres/', data=data)
    return result


def create_titles(admin_client):
    genres = create_genre(admin_client)
    categories = create_categories(admin_client)
    result = []
    data = {'name': 'Поворот туда', 'year': 2000, 'genre': [genres[0]['slug'], genres[1]['slug']],
            'category': categories[0]['slug'], 'description': 'Крутое пике'}
    response = admin_client.post('/api/v1/titles/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    data = {'name': 'Проект', 'year': 2020, 'genre': [genres[2]['slug']], 'category': categories[1]['slug'],
            'description': 'Главная драма года'}
    response = admin_client.post('/api/v1/titles/', data=data)
    data['id'] = response.json()['id']
    result.append(data)
    return result, categories, genres


def create_reviews(admin_client, admin):
    def create_review(uclient, title_id, text, score):
        data = {'text': text, 'score': score}
        response = uclient.post(f'/api/v1/titles/{title_id}/reviews/', data=data)
        return response.json()['id']

    titles, _, _ = create_titles(admin_client)
    user, moderator = create_users_api(admin_client)
    client_user = auth_client(user)
    client_moderator = auth_client(moderator)
    result = list()
    result.append({'id': create_review(admin_client, titles[0]["id"], 'qwerty', 5),
                   'author': admin.username, 'text': 'qwerty', 'score': 5})
    result.append({'id': create_review(client_user, titles[0]["id"], 'qwerty123', 3),
                   'author': user.username, 'text': 'qwerty123', 'score': 3})
    result.append({'id': create_review(client_moderator, titles[0]["id"], 'qwerty321', 4),
                   'author': moderator.username, 'text': 'qwerty321', 'score': 4})
    return result, titles, user, moderator


def create_comments(admin_client, admin):
    def create_comment(uclient, title_id, review_id, text):
        data = {'text': text}
        response = uclient.post(f'/api/v1/titles/{title_id}/reviews/{review_id}/comments/', data=data)
        return response.json()['id']

    reviews, titles, user, moderator = create_reviews(admin_client, admin)
    client_user = auth_client(user)
    client_moderator = auth_client(moderator)
    result = list()
    result.append({'id': create_comment(admin_client, titles[0]["id"], reviews[0]["id"], 'qwerty'),
                   'author': admin.username, 'text': 'qwerty'})
    result.append({'id': create_comment(client_user, titles[0]["id"], reviews[0]["id"], 'qwerty123'),
                   'author': user.username, 'text': 'qwerty123'})
    result.append({'id': create_comment(client_moderator, titles[0]["id"], reviews[0]["id"], 'qwerty321'),
                   'author': moderator.username, 'text': 'qwerty321'})
    return result, reviews, titles, user, moderator
