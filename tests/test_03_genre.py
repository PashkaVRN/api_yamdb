import pytest

from .common import auth_client, create_genre, create_users_api


class Test03GenreAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_genre_not_auth(self, client):
        response = client.get('/api/v1/genres/')
        assert response.status_code != 404, (
            'Страница `/api/v1/genres/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/genres/` без токена авторизации возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_genre(self, admin_client):
        data = {}
        response = admin_client.post('/api/v1/genres/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/genres/` с не правильными данными возвращает статус 400'
        )
        data = {'name': 'Ужасы', 'slug': 'horror'}
        response = admin_client.post('/api/v1/genres/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/genres/` с правильными данными возвращает статус 201'
        )
        data = {'name': 'Триллер', 'slug': 'horror'}
        response = admin_client.post('/api/v1/genres/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/genres/` нельзя создать 2 жанра с одинаковым `slug`'
        )
        data = {'name': 'Комедия', 'slug': 'comedy'}
        response = admin_client.post('/api/v1/genres/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/genres/` с правильными данными возвращает статус 201'
        )
        response = admin_client.get('/api/v1/genres/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращает статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 2, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert len(data['results']) == 2, (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )
        assert {'name': 'Ужасы', 'slug': 'horror'} in data['results'], (
            'Проверьте, что при GET запросе `/api/v1/genres/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )
        response = admin_client.get('/api/v1/genres/?search=Ужасы')
        data = response.json()
        assert len(data['results']) == 1, (
            'Проверьте, что при GET запросе `/api/v1/genres/` фильтуется по search параметру названия жанра '
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_genres_delete(self, admin_client):
        genres = create_genre(admin_client)
        response = admin_client.delete(f'/api/v1/genres/{genres[0]["slug"]}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/v1/genres/{slug}/` возвращаете статус 204'
        )
        response = admin_client.get('/api/v1/genres/')
        test_data = response.json()['results']
        assert len(test_data) == len(genres) - 1, (
            'Проверьте, что при DELETE запросе `/api/v1/genres/{slug}/` удаляете жанр '
        )
        response = admin_client.get(f'/api/v1/genres/{genres[0]["slug"]}/')
        assert response.status_code == 405, (
            'Проверьте, что при GET запросе `/api/v1/genres/{slug}/` возвращаете статус 405'
        )
        response = admin_client.patch(f'/api/v1/genres/{genres[0]["slug"]}/')
        assert response.status_code == 405, (
            'Проверьте, что при PATCH запросе `/api/v1/genres/{slug}/` возвращаете статус 405'
        )

    def check_permissions(self, user, user_name, genres):
        client_user = auth_client(user)
        data = {
            'name': 'Боевик',
            'slug': 'action'
        }
        response = client_user.post('/api/v1/genres/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при POST запросе `/api/v1/genres/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        response = client_user.delete(f'/api/v1/genres/{genres[0]["slug"]}/')
        assert response.status_code == 403, (
            f'Проверьте, что при DELETE запросе `/api/v1/genres/{{slug}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_genres_check_permission(self, client, admin_client):
        genres = create_genre(admin_client)
        data = {
            'name': 'Боевик',
            'slug': 'action'
        }
        response = client.post('/api/v1/genres/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/v1/genres/` '
            'без токена авторизации возвращается статус 401'
        )
        response = client.delete(f'/api/v1/genres/{genres[0]["slug"]}/')
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе `/api/v1/genres/{{slug}}/` '
            'без токена авторизации возвращается статус 401'
        )
        user, moderator = create_users_api(admin_client)
        self.check_permissions(user, 'обычного пользователя', genres)
        self.check_permissions(moderator, 'модератора', genres)

    @pytest.mark.django_db(transaction=True)
    def test_05_genre_create_user(self, user_client):
        url = '/api/v1/genres/'
        data = {
            'name': 'Всякое разное',
            'slug': 'something'
        }
        response = user_client.post(url, data=data)
        code = 403
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе на `{url}`, создание жанров недоступно для '
            f'пользователя с ролью user'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_genre_create_moderator(self, moderator_client):
        url = '/api/v1/genres/'
        data = {
            'name': 'Всякое разное',
            'slug': 'something'
        }
        response = moderator_client.post(url, data=data)
        code = 403
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе на `{url}`, создание жанров недоступно для '
            f'пользователя с ролью moderator'
        )
