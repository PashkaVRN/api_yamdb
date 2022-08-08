import pytest


@pytest.fixture
def user_superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestSuperuser', email='testsuperuser@yamdb.fake', password='1234567', role='user', bio='superuser bio'
    )


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        username='TestAdmin', email='testadmin@yamdb.fake', password='1234567', role='admin', bio='admin bio'
    )


@pytest.fixture
def moderator(django_user_model):
    return django_user_model.objects.create_user(
        username='TestModerator', email='testmoder@yamdb.fake', password='1234567', role='moderator', bio='moder bio'
    )


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser', email='testuser@yamdb.fake', password='1234567', role='user', bio='user bio'
    )


@pytest.fixture
def token_user_superuser(user_superuser):
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(user_superuser)

    return {
        'access': str(token),
    }


@pytest.fixture
def user_superuser_client(token_user_superuser):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user_superuser["access"]}')
    return client


@pytest.fixture
def token_admin(admin):
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(admin)

    return {
        'access': str(token),
    }


@pytest.fixture
def admin_client(token_admin):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_admin["access"]}')
    return client


@pytest.fixture
def token_moderator(moderator):
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(moderator)

    return {
        'access': str(token),
    }


@pytest.fixture
def moderator_client(token_moderator):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_moderator["access"]}')
    return client


@pytest.fixture
def token_user(user):
    from rest_framework_simplejwt.tokens import AccessToken
    token = AccessToken.for_user(user)

    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(token_user):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client
