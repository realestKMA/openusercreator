from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework import status
import pytest


User = get_user_model()
create_url = reverse('creators_create', kwargs={'version': 'v1'})
# login_session_url = reverse('login_via_session', kwargs={'version': 'v1'})
login_token_url = reverse('login_via_token', kwargs={'version': 'v1'})
my_data_url = reverse('creators_details', kwargs={'version': 'v1'})
update_data_url = reverse('creators_update', kwargs={'version': 'v1'})
change_password_url = reverse('creators_change_password', kwargs={'version': 'v1'})
verify_toke_url = reverse('token_verify', kwargs={'version': 'v1'})
refresh_toke_url = reverse('token_refresh', kwargs={'version': 'v1'})
list_creators_url = reverse('creators_list', kwargs={'version': 'v1'})
delete_data_url = reverse('creators_delete', kwargs={'version': 'v1'})


@pytest.mark.django_db
def test_create_new_account_and_check_that_no_sensitive_data_is_returned(full_user_data):
    client = APIClient(enforce_csrf_checks=True)

    # GET request method not allowed
    res = client.get(create_url)
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert 'Method \"GET\" not allowed' in res.data['detail']

    # make POST request with no data
    res = client.post(create_url, format='json')
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # make POST request with data
    res = client.post(create_url, full_user_data, format='json')

    assert res.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1
    assert res.data['user']['username'] == full_user_data['username'].lower()
    assert res.data['user']['email'] == full_user_data['email'].lower()
    assert res.data['user']['first_name'] == full_user_data['first_name']
    assert res.data['user']['last_name'] == full_user_data['last_name']
    assert res.data['user']['other_name'] == full_user_data['other_name']
    assert len(res.data['user']['uid']) == 20
    assert str(res.data['user']['uid']).isnumeric()
    assert not res.data['user']['is_verified']
    assert 'password' not in res.data['user']
    assert res.data['user']['date_joined']
    assert res.data['user']['last_login'] is None


# @pytest.mark.django_db
# def test_new_creators_can_login_via_session(full_user_data):
#     client = APIClient(enforce_csrf_checks=True)

#     # GET request method not allowed
#     res = client.get(login_session_url)
#     assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
#     assert 'Method \"GET\" not allowed' in res.data['detail']

#     # make POST request with no data
#     res = client.post(login_session_url, format='json')
#     assert res.status_code == status.HTTP_400_BAD_REQUEST

#     # register new user first
#     res = client.post(create_url, full_user_data, format='json')
#     assert res.status_code == status.HTTP_201_CREATED
#     assert User.objects.count() == 1

#     # now login the new user via session login
#     res = client.post(login_session_url, full_user_data, format='json')

#     assert res.status_code == status.HTTP_200_OK
#     assert 'Logged in successfully' in res.data['detail']
#     assert res.cookies['csrftoken']
#     assert res.cookies['sessionid']


@pytest.mark.django_db
def test_creators_can_login_via_token(full_user_data):
    client = APIClient(enforce_csrf_checks=True)

    # GET request method not allowed
    res = client.get(login_token_url)
    assert res.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    assert 'Method \"GET\" not allowed' in res.data['detail']

    # make POST request with no data
    res = client.post(login_token_url)
    assert res.status_code == status.HTTP_400_BAD_REQUEST

    # register new user first
    res = client.post(create_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

    # now login the new user via token login
    res = client.post(login_token_url, full_user_data, format='json')

    assert res.status_code == status.HTTP_200_OK
    assert 'access' in res.data
    assert 'refresh' in res.data


@pytest.mark.django_db
def test_creators_detail_endpoint_returns_currently_logged_in_users_data(created, full_user_data):
    client = APIClient(enforce_csrf_checks=True)

    # because of the created fixture
    assert User.objects.count() == 1

    # now login the user
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # get users data
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.get(my_data_url)
    assert res.status_code == status.HTTP_200_OK
    assert res.data['username'] == full_user_data['username'].lower()
    assert res.data['email'] == full_user_data['email'].lower()
    assert res.data['first_name'] == full_user_data['first_name']
    assert res.data['last_name'] == full_user_data['last_name']
    assert res.data['other_name'] == full_user_data['other_name']
    assert len(res.data['uid']) == 20
    assert str(res.data['uid']).isnumeric()
    assert not res.data['is_verified']
    assert 'password' not in res.data
    assert res.data['date_joined'] is not None
    assert res.data['last_login'] is not None


@pytest.mark.django_db
def test_unauthenticated_request_on_creators_details_endpoint_should_fail():
    client = APIClient(enforce_csrf_checks=True)

    res = client.get(my_data_url)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'Authentication credentials were not provided' in res.data['detail']


@pytest.mark.django_db
def test_autenticated_users_can_update_their_data(created, full_user_data, another_user_data):
    client = APIClient(enforce_csrf_checks=True)

    # because of the created fixture
    assert User.objects.count() == 1

    # now login the user, using full_user_data fixture used in the created fixture
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # now, update the users data
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.put(update_data_url, another_user_data, format='json')

    assert res.status_code == status.HTTP_202_ACCEPTED
    assert res.data['username'] == another_user_data['username'].lower()
    assert res.data['email'] == another_user_data['email'].lower()
    assert res.data['first_name'] == another_user_data['first_name']
    assert res.data['last_name'] == another_user_data['last_name']
    assert res.data['other_name'] == another_user_data['other_name']
    assert res.data['uid'] not in ['', None]
    assert not res.data['is_verified']
    assert 'password' not in res.data
    assert res.data['date_joined'] is not None
    assert res.data['last_login'] is not None


@pytest.mark.django_db
def test_autenticated_users_can_delete_their_account(created, full_user_data):
    client = APIClient(enforce_csrf_checks=True)

    # because of the created fixture
    assert User.objects.count() == 1

    # now login the user, using full_user_data fixture used in the created fixture
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # get the users data to compare with the deleted response data
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.get(my_data_url)
    assert res.status_code == status.HTTP_200_OK

    user_data = res.data

    # now delete the currently logged in user account
    res = client.delete(delete_data_url)

    assert res.status_code == status.HTTP_204_NO_CONTENT
    assert 'Deleted successfully' in res.data['detail']
    assert res.data['uid'] == user_data['uid']
    assert res.data['username'] == user_data['username']
    assert res.data['email'] == user_data['email']


@pytest.mark.django_db
def test_only_admin_users_can_retrieve_all_creators(
    full_user_data,
    test_user_1,
    created,
    created_superuser
                    ):
    client = APIClient(enforce_csrf_checks=True)

    # because of the created and created_superuser fixture
    assert User.objects.count() == 2

    # now, authenticate the non admin user
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # now calling the creator_list endpoint with the non admin user should be forbidden
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.get(list_creators_url)
    assert res.status_code == status.HTTP_403_FORBIDDEN

    # now, authenticate the user with admin privilege
    res = client.post(login_token_url, test_user_1)
    assert res.status_code == status.HTTP_200_OK

    # now calling the creator_list endpoint should pass
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.get(list_creators_url)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 2


@pytest.mark.django_db
def test_authenticated_creators_can_change_their_password(created, full_user_data):
    client = APIClient()

    # because of the created fixture
    assert User.objects.count() == 1

    # now, authenticate the user
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # change password
    data = {
        "old_password": "fufu@6060f914",
        "new_password1": "mynewpassword",
        "new_password2": "mynewpassword"
    }

    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.post(change_password_url, data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # now authenticate with the new password
    res = client.post(
        login_token_url,
        {'username': full_user_data['username'].lower(), 'password': 'mynewpassword'},
        format='json'
    )
    assert res.status_code == status.HTTP_200_OK


# @pytest.mark.django_db
# def test_authentication_via_session_will_clear_the_access_and_refreshs_of_users_who_were_authenticated_via_token(
#     created,
#     full_user_data
#         ):
#     client = APIClient()

#     # because of the created fixture
#     assert User.objects.count() == 1

#     # now authenticate via token first
#     res = client.post(login_token_url, full_user_data, format='json')
#     assert res.status_code == status.HTTP_200_OK
#     assert res.data['access']
#     assert res.data['refresh']

#     # now authenticate via session
#     res = client.post(login_session_url, full_user_data, format='json')
#     assert res.status_code == status.HTTP_200_OK
#     assert res.cookies['csrftoken']
#     assert res.cookies['sessionid']
#     assert 'access' not in res.data
#     assert 'refresh' not in res.data


@pytest.mark.django_db
def test_verify_token_url_verifies_token_authenticity(created, full_user_data):
    client = APIClient()

    # because of the created fixture
    assert User.objects.count() == 1

    # now authenticate user via token
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    # now, verify token
    client.credentials(HTTP_AUTHORIZATION=F"Bearer {res.data['access']}")
    res = client.post(verify_toke_url, {"token": res.data['access']}, format='json')
    assert res.status_code == status.HTTP_200_OK
    assert res.data == {}


@pytest.mark.django_db
def test_refresh_token_url_refreshes_auth_token(created, full_user_data):
    """
    Takes the refresh token and refreshes the access token
    """
    client = APIClient()

    # because of the created fixture
    assert User.objects.count() == 1

    # now authenticate user via token
    res = client.post(login_token_url, full_user_data, format='json')
    assert res.status_code == status.HTTP_200_OK

    refresh = res.data['refresh']

    # now, refresh token
    # client.credentials(HTTP_AUTHORIZATION=F'Bearer {jwt}')
    res = client.post(refresh_toke_url, {'refresh': refresh})
    assert res.status_code == status.HTTP_200_OK
    assert 'access' in res.data
