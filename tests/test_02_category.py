import pytest

from .common import auth_client, create_categories, create_users_api


class Test02CategoryAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_category_not_auth(self, client):
        response = client.get('/api/v1/categories/')
        assert response.status_code != 404, (
            'Страница `/api/v1/categories/` не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/categories/` без токена авторизации возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_category_admin(self, admin_client):
        data = {}
        response = admin_client.post('/api/v1/categories/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/categories/` с не правильными данными возвращает статус 400'
        )
        data = {
            'name': 'Фильм',
            'slug': 'films'
        }
        response = admin_client.post('/api/v1/categories/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/categories/` с правильными данными возвращает статус 201'
        )
        data = {
            'name': 'Новые фильмы',
            'slug': 'films'
        }
        response = admin_client.post('/api/v1/categories/', data=data)
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/categories/` нельзя создать 2 категории с одинаковым `slug`'
        )
        data = {
            'name': 'Книги',
            'slug': 'books'
        }
        response = admin_client.post('/api/v1/categories/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/categories/` с правильными данными возвращает статус 201'
        )
        response = admin_client.get('/api/v1/categories/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращает статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Не найден параметр `results`'
        )
        assert data['count'] == 2, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Тип параметра `results` должен быть список'
        )
        assert len(data['results']) == 2, (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )
        assert {'name': 'Книги', 'slug': 'books'} in data['results'], (
            'Проверьте, что при GET запросе `/api/v1/categories/` возвращаете данные с пагинацией. '
            'Значение параметра `results` не правильное'
        )
        response = admin_client.get('/api/v1/categories/?search=Книги')
        data = response.json()
        assert len(data['results']) == 1, (
            'Проверьте, что при GET запросе `/api/v1/categories/` фильтуется по search параметру названия категории'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_category_delete_admin(self, admin_client):
        create_categories(admin_client)
        response = admin_client.delete('/api/v1/categories/books/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/v1/categories/{slug}/` возвращаете статус 204'
        )
        response = admin_client.get('/api/v1/categories/')
        test_data = response.json()['results']
        assert len(test_data) == 1, (
            'Проверьте, что при DELETE запросе `/api/v1/categories/{slug}/` удаляете категорию '
        )
        response = admin_client.get('/api/v1/categories/books/')
        code = 405
        assert response.status_code == code, (
            'Проверьте, что при GET запросе `/api/v1/categories/{slug}/` '
            f'возвращаете статус {code}'
        )
        response = admin_client.patch('/api/v1/categories/books/')
        assert response.status_code == code, (
            'Проверьте, что при PATCH запросе `/api/v1/categories/{slug}/` '
            f'возвращаете статус {code}'
        )

    def check_permissions(self, user, user_name, categories):
        client_user = auth_client(user)
        data = {
            'name': 'Музыка',
            'slug': 'music'
        }
        response = client_user.post('/api/v1/categories/', data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при POST запросе `/api/v1/categories/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        response = client_user.delete(f'/api/v1/categories/{categories[0]["slug"]}/')
        assert response.status_code == 403, (
            f'Проверьте, что при DELETE запросе `/api/v1/categories/{{slug}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_category_check_permission_admin(self, client, admin_client):
        categories = create_categories(admin_client)
        data = {
            'name': 'Музыка',
            'slug': 'music'
        }
        response = client.post('/api/v1/categories/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/v1/categories/` '
            'без токена авторизации возвращается статус 401'
        )
        response = client.delete(f'/api/v1/categories/{categories[0]["slug"]}/')
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе `/api/v1/categories/{{slug}}/` '
            'без токена авторизации возвращается статус 401'
        )
        user, moderator = create_users_api(admin_client)
        self.check_permissions(user, 'обычного пользователя', categories)
        self.check_permissions(moderator, 'модератора', categories)

    @pytest.mark.django_db(transaction=True)
    def test_05_category_create_user(self, user_client):
        url = '/api/v1/categories/'
        data = {
            'name': 'Всякое разное',
            'slug': 'something'
        }
        response = user_client.post(url, data=data)
        code = 403
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе на `{url}`, создание категорий недоступно для '
            f'пользователя с ролью user'
        )

    @pytest.mark.django_db(transaction=True)
    def test_06_category_create_moderator(self, moderator_client):
        url = '/api/v1/categories/'
        data = {
            'name': 'Всякое разное',
            'slug': 'something'
        }
        response = moderator_client.post(url, data=data)
        code = 403
        assert response.status_code == code, (
            f'Проверьте, что при POST запросе на `{url}`, создание категорий недоступно для '
            f'пользователя с ролью moderator'
        )
