import pytest

from .common import auth_client, create_comments, create_reviews


class Test06CommentAPI:

    @pytest.mark.django_db(transaction=True)
    def test_01_comment_not_auth(self, client, admin_client, admin):
        reviews, titles, _, _ = create_reviews(admin_client, admin)
        response = client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/')
        assert response.status_code != 404, (
            'Страница `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'без токена авторизации возвращается статус 200'
        )

    def create_comment(self, client_user, title_id, review_id, text):
        data = {'text': text}
        response = client_user.post(f'/api/v1/titles/{title_id}/reviews/{review_id}/comments/', data=data)
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'с правильными данными возвращает статус 201, api доступен для любого аутентифицированного пользователя'
        )
        return response

    @pytest.mark.django_db(transaction=True)
    def test_02_comment(self, admin_client, admin):
        reviews, titles, user, moderator = create_reviews(admin_client, admin)
        client_user = auth_client(user)
        client_moderator = auth_client(moderator)
        data = {}
        response = admin_client.post(
            f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/', data=data
        )
        assert response.status_code == 400, (
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'с не правильными данными возвращает статус 400'
        )
        self.create_comment(admin_client, titles[0]["id"], reviews[0]["id"], 'qwerty')
        self.create_comment(client_user, titles[0]["id"], reviews[0]["id"], 'qwerty123')
        self.create_comment(client_moderator, titles[0]["id"], reviews[0]["id"], 'qwerty321')

        self.create_comment(admin_client, titles[0]["id"], reviews[1]["id"], 'qwerty432')
        self.create_comment(client_user, titles[0]["id"], reviews[1]["id"], 'qwerty534')
        response = self.create_comment(client_moderator, titles[0]["id"], reviews[1]["id"], 'qwerty231')

        assert type(response.json().get('id')) == int, (
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные созданного объекта. Значение `id` нет или не является целым числом.'
        )

        data = {'text': 'kjdfg'}
        response = admin_client.post('/api/v1/titles/999/reviews/999/comments/', data=data)
        assert response.status_code == 404, (
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'с не существующим title_id или review_id возвращается статус 404.'
        )
        data = {'text': 'аывв'}
        response = admin_client.post(
            f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/', data=data
        )
        assert response.status_code == 201, (
            'Проверьте, что при POST запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'на отзыв можно оставить несколько комментариев.'
        )

        response = admin_client.get(f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращает статус 200'
        )
        data = response.json()
        assert 'count' in data, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Не найден параметр `count`'
        )
        assert 'next' in data, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Не найден параметр `next`'
        )
        assert 'previous' in data, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Не найден параметр `previous`'
        )
        assert 'results' in data, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Не найден параметр `results`'
        )
        assert data['count'] == 4, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Значение параметра `count` не правильное'
        )
        assert type(data['results']) == list, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Тип параметра `results` должен быть список'
        )
        assert len(data['results']) == 4, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Значение параметра `results` не правильное'
        )

        comment = None
        for item in data['results']:
            if item.get('text') == 'qwerty':
                comment = item
        assert comment, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. Значение параметра `results` неправильное, '
            '`text` не найдено или не сохранилось при POST запросе.'
        )
        assert comment.get('author') == admin.username, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. '
            'Значение параметра `results` неправильное, `author` не найдено или не сохранилось при POST запросе.'
        )
        assert comment.get('pub_date'), (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/`'
            ' возвращаете данные с пагинацией. Значение параметра `results` неправильное, `pub_date` не найдено.'
        )
        assert type(comment.get('id')) == int, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/` '
            'возвращаете данные с пагинацией. '
            'Значение параметра `results` неправильное, значение `id` нет или не является целым числом.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_review_detail(self, client, admin_client, admin):
        comments, reviews, titles, user, moderator = create_comments(admin_client, admin)
        pre_url = f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/'
        response = client.get(f'{pre_url}{comments[0]["id"]}/')
        assert response.status_code != 404, (
            'Страница `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'не найдена, проверьте этот адрес в *urls.py*'
        )
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'без токена авторизации возвращается статус 200'
        )
        data = response.json()
        assert type(data.get('id')) == int, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете данные объекта. Значение `id` нет или не является целым числом.'
        )
        assert data.get('text') == reviews[0]['text'], (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете данные объекта. Значение `text` неправильное.'
        )
        assert data.get('author') == reviews[0]['author'], (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете данные объекта. Значение `author` неправильное.'
        )

        data = {'text': 'rewq'}
        response = admin_client.patch(f'{pre_url}{comments[0]["id"]}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращается статус 200'
        )
        data = response.json()
        assert data.get('text') == 'rewq', (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете данные объекта. Значение `text` изменено.'
        )
        response = admin_client.get(f'{pre_url}{comments[0]["id"]}/')
        assert response.status_code == 200, (
            'Проверьте, что при GET запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'без токена авторизации возвращается статус 200'
        )
        data = response.json()
        assert data.get('text') == 'rewq', (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'изменяете значение `text`.'
        )

        client_user = auth_client(user)
        data = {'text': 'fgf'}
        response = client_user.patch(f'{pre_url}{comments[2]["id"]}/', data=data)
        assert response.status_code == 403, (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'от обычного пользователя при попытки изменить не свой отзыв возвращается статус 403'
        )

        data = {'text': 'jdfk'}
        response = client_user.patch(f'{pre_url}{comments[1]["id"]}/', data=data)
        assert response.status_code == 200, (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращается статус 200'
        )
        data = response.json()
        assert data.get('text') == 'jdfk', (
            'Проверьте, что при PATCH запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете данные объекта. Значение `text` изменено.'
        )

        client_moderator = auth_client(moderator)
        response = client_moderator.delete(f'{pre_url}{comments[1]["id"]}/')
        assert response.status_code == 204, (
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'возвращаете статус 204'
        )
        response = admin_client.get(f'{pre_url}')
        test_data = response.json()['results']
        assert len(test_data) == len(comments) - 1, (
            'Проверьте, что при DELETE запросе `/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/` '
            'удаляете объект'
        )

    def check_permissions(self, user, user_name, pre_url):
        client_user = auth_client(user)
        data = {'text': 'jdfk'}
        response = client_user.patch(pre_url, data=data)
        assert response.status_code == 403, (
            f'Проверьте, что при PATCH запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )
        response = client_user.delete(pre_url)
        assert response.status_code == 403, (
            f'Проверьте, что при DELETE запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/` '
            f'с токеном авторизации {user_name} возвращается статус 403'
        )

    @pytest.mark.django_db(transaction=True)
    def test_04_comment_check_permission(self, client, admin_client, admin):
        comments, reviews, titles, user, moderator = create_comments(admin_client, admin)
        pre_url = f'/api/v1/titles/{titles[0]["id"]}/reviews/{reviews[0]["id"]}/comments/'
        data = {'text': 'jdfk'}
        response = client.post(f'{pre_url}', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при POST запросе `/api/v1/titles/{{title_id}}/reviews/{{review_id}}/comments/` '
            'без токена авторизации возвращается статус 401'
        )
        response = client.patch(f'{pre_url}{comments[1]["id"]}/', data=data)
        assert response.status_code == 401, (
            'Проверьте, что при PATCH запросе '
            '`/api/v1/titles/{{title_id}}/reviews/{{review_id}}/comments/{{comment_id}}/` '
            'без токена авторизации возвращается статус 401'
        )
        response = client.delete(f'{pre_url}{comments[1]["id"]}/')
        assert response.status_code == 401, (
            'Проверьте, что при DELETE запросе '
            '`/api/v1/titles/{{title_id}}/reviews/{{review_id}}/comments/{{comment_id}}/` '
            'без токена авторизации возвращается статус 401'
        )
        self.check_permissions(user, 'обычного пользователя', f'{pre_url}{comments[2]["id"]}/')
