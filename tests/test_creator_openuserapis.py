from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from django.utils.timezone import datetime
from rest_framework.test import APIClient
from creator.models import Openuser
from rest_framework import status
import pytest

# Custom user model
AppUser = get_user_model()

# urls
list_my_openusers_url = reverse('creators_apps', kwargs={'version': 'v1'})
create_openuser_url = reverse('creators_apps_create', kwargs={'version': 'v1'})
# get_an_openuser_url = reverse('creators_apps_detail', kwargs={'version': 'v1'})
# update_openuser_url = reverse('creators_apps_update', kwargs={'version': 'v1'})
# delete_openuser_url = reverse('creators_apps_delete', kwargs={'version': 'v1'})
create_user_url = reverse('creators_create', kwargs={'version': 'v1'})
login_token_url = reverse('login_via_token', kwargs={'version': 'v1'})


class TestCase:

    @pytest.mark.django_db
    def test_unauthenticated_users_cannot_create_an_openuser_profile(self, openuser_data_1):
        client = APIClient()

        assert Openuser.objects.count() == 0

        res = client.post(create_openuser_url, openuser_data_1, format='json')
        assert res.status_code == status.HTTP_401_UNAUTHORIZED
        assert 'Authentication credentials were not provided' in res.data['detail']

    @pytest.mark.django_db
    def test_authenticated_users_can_create_openuser_profiles(self, created, full_user_data, openuser_data_1):
        client = APIClient()

        # because of the created fixture
        assert AppUser.objects.count() == 1

        # no record yet
        assert Openuser.objects.count() == 0

        # we need to login
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert 'access_token' in res.data
        assert 'refresh_token' in res.data

        # since we are now logged in, create a new openuser profile
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.post(create_openuser_url, openuser_data_1, format='json')
        assert res.status_code == status.HTTP_201_CREATED
        assert Openuser.objects.count() == 1
        assert isinstance(res.data['data']['id'], int)
        assert res.data['data']['creator'] == created.username
        assert res.data['data']['name'] == openuser_data_1['name'].lower()
        assert res.data['data']['profiles'] == openuser_data_1['profiles']
        assert res.data['data']['profile_password'] == openuser_data_1['profile_password']
        assert res.data['data']['date_created'] not in ['', None]
        assert res.data['data']['last_updated'] not in ['', None]

    @pytest.mark.django_db()
    def test_authenticated_users_cannot_create_openuser_profiles_with_same_name(
        self,
        created,
        full_user_data,
        openuser_data_1
            ):
        client = APIClient()

        # because of the created fixture
        assert AppUser.objects.count() == 1

        # no record yet
        assert Openuser.objects.count() == 0

        # we need to login
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # create a new openuser profile
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.post(create_openuser_url, openuser_data_1, format='json')
        assert res.status_code == status.HTTP_201_CREATED
        assert Openuser.objects.count() == 1

        # now try to create another openuser profile with the same name.
        res = client.post(create_openuser_url, openuser_data_1, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'You already have an app with that name' in str(res.data['error'])

    @pytest.mark.django_db
    def test_list_endpoint_returns_openuser_profiles_of_the_authenticated_request_user_only(
        self,
        created,
        full_user_data,
        created_user,
        test_user_1,
        created_openuser_1,
        created_openuser_2,
        created_openuser_3,
        created_openuser_4,
        created_openuser_5,
        created_openuser_6,
            ):
        client = APIClient()

        # because of the created and created_user fixtures
        assert AppUser.objects.count() == 2
        # and also the *_openusers fixture
        assert Openuser.objects.count() == 6

        # now login with the created fixture details
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # return all openuser profile, assert that all returned data belongs to the
        # currently authenticated user
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.get(list_my_openusers_url, format='json')
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data['data']) == 3
        assert res.data['data'][0]['creator'] == created.username
        assert res.data['data'][1]['creator'] == created.username
        assert res.data['data'][2]['creator'] == created.username

    @pytest.mark.django_db
    def test_authenticated_users_can_only_retireve_an_instance_of_their_openuser_app(
        self,
        created,
        full_user_data,
        created_user,
        test_user_1,
        created_openuser_1,
        created_openuser_2,
        created_openuser_3,
        created_openuser_4,
        created_openuser_5,
        created_openuser_6
            ):
        """
        NOTE: THe fixtures created_openuser_1,2 and 3 has the same name value as created_openuser_4,5 and 6
        respectively. But belongs to 2 different creators. The full_user_data fixture data was use as the
        data to create the created user fixture, while the test_user_1 fixture data was used to create the
        created_user user fixture.
        """
        client = APIClient()

        # because of the created and created_user fixtures
        assert AppUser.objects.count() == 2
        # and also the *_openusers_* fixture
        assert Openuser.objects.count() == 6

        # now login with the created fixture details
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # retrieve an instace of the openuser app for the created user
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.get(
            reverse(
                'creators_apps_detail',
                kwargs={'version': 'v1', 'name': F'{created_openuser_2.name.lower()}'},
            ))

        assert res.status_code == status.HTTP_200_OK
        assert len(res.data) == 1
        assert res.data['data']['id'] == created_openuser_2.id
        assert res.data['data']['name'] == created_openuser_2.name.lower()
        assert res.data['data']['creator'] == created_openuser_2.creator.username
        assert res.data['data']['profiles'] == created_openuser_2.profiles
        assert res.data['data']['profile_password'] == created_openuser_2.profile_password
        assert datetime.fromisoformat(res.data['data']['date_created']) == created_openuser_2.date_created
        assert datetime.fromisoformat(res.data['data']['last_updated']) == created_openuser_2.last_updated

    @pytest.mark.django_db
    def test_openuser_name_field_must_obey_the_validators_applied(self, created, full_user_data):
        """
        NOTE: The name field must start and end with a letter, and can only contain letters, numbers,
        and hyphens. Underscores are converted to spaces tooa dn the whole string is converted to
        lowercase.
        """
        client = APIClient()

        # because of the created fixtures
        assert AppUser.objects.count() == 1

        # login user
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # now try to create a new openuser profile with a name field containing
        # characters not allowed
        data_1 = dict(
            name='1cannotwork',  # should not start with a number
            profiles=4,
            profile_password="P@ssw0rd"
        )

        data_2 = dict(
            name='anotherillegal1',  # should not end with number
            profiles=44,
            profile_password="P@ssw0rd"
        )

        data_3 = dict(
            name='please@not',  # wont work either
            profiles=35,
            profile_password="P@ssw0rd"
        )

        data_4 = dict(
            name='space in between',  # will work
            profiles=45,
            profile_password="P@ssw0rd"
        )

        data_5 = dict(
            name='not',  # should not be less than 4 characters
            profiles=45,
            profile_password="P@ssw0rd"
        )

        data_6 = dict(
            name='theNameFieldShoulNotBeMoreThan20CharactersLong',
            profiles=45,
            profile_password="P@ssw0rd"
        )

        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')

        # create with data_1
        res = client.post(create_openuser_url, data_1, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Must begin and end with a letter' in str(res.data['name'])

        # create with data_2
        res = client.post(create_openuser_url, data_2, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Must begin and end with a letter' in str(res.data['name'])

        # create with data_3
        res = client.post(create_openuser_url, data_3, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'can only contain letters, numbers and hyphens' in str(res.data['name'])

        # create with data_4
        res = client.post(create_openuser_url, data_4, format='json')
        assert res.status_code == status.HTTP_201_CREATED
        assert res.data['data']['name'] == data_4['name'].replace(' ', '-').lower()

        # create with data_5
        res = client.post(create_openuser_url, data_5, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Ensure this field has at least 4 characters' in str(res.data['name'])

        # create with data_6
        res = client.post(create_openuser_url, data_6, format='json')
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Ensure this field has no more than 20 characters' in str(res.data['name'])

    @pytest.mark.django_db
    def test_authenticated_users_can_update_their_openuser_profiles(self, created, openuser_data_1, full_user_data):
        client = APIClient()

        # because of the created fixtures
        assert AppUser.objects.count() == 1
        # and also the *_openusers_* fixture
        assert Openuser.objects.count() == 0

        # login user
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # create an openuser data
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.post(create_openuser_url, openuser_data_1, format='json')
        assert res.status_code == status.HTTP_201_CREATED

        # get the newly created openuser object
        res = client.get(
            reverse(
                'creators_apps_detail',
                kwargs={'version': 'v1', 'name': F'{openuser_data_1["name"].lower()}'},
            ))
        old_data = res.data['data']

        new_date = dict(
            name='Update-1-Api',
            profiles=22,
            profile_password="Myp@ssw0rd",
        )

        # now, update that particular openuser object with the new_data
        res = client.put(
            reverse(
                'creators_apps_update',
                kwargs={'version': 'v1', 'name': F'{openuser_data_1["name"].lower()}'},
            ),
            new_date,
            format='json'
        )

        assert res.status_code == status.HTTP_200_OK
        assert res.data['data']['id'] == old_data['id']
        assert res.data['data']['creator'] == old_data['creator']
        assert res.data['data']['creator'] == created.username
        assert res.data['data']['name'] != old_data['name']
        assert res.data['data']['profiles'] != old_data['profiles']
        assert res.data['data']['profile_password'] != old_data['profile_password']
        assert res.data['data']['name'] == new_date['name'].lower()
        assert res.data['data']['profiles'] == new_date['profiles']
        assert res.data['data']['profile_password'] == new_date['profile_password']

    @pytest.mark.django_db
    def test_authenticated_users_can_delete_an_openuser_instance(
        self,
        created,
        full_user_data,
        created_openuser_1,
        created_openuser_2,
        created_openuser_3,
            ):
        client = APIClient()

        # because of the created fixtures
        assert AppUser.objects.count() == 1
        # and also the *_openusers_* fixture
        assert Openuser.objects.count() == 3

        # login user
        res = client.post(login_token_url, full_user_data, format='json')
        assert res.status_code == status.HTTP_200_OK

        # get all openuser objects created by the currently logged in user
        client.credentials(HTTP_AUTHORIZATION=F'Bearer {res.cookies["jwt-access"].value}')
        res = client.get(list_my_openusers_url)
        assert res.status_code == status.HTTP_200_OK
        assert len(res.data['data']) == 3

        # now delete one openuser instance
        res = client.delete(
            reverse(
                'creators_apps_delete',
                kwargs={'version': 'v1', 'name': created_openuser_2.name.lower()}
            ),
            format='json'
        )
        assert res.status_code == status.HTTP_204_NO_CONTENT
        assert Openuser.objects.count() == 2
        assert res.data['data']['name'] == created_openuser_2.name.lower()
        assert res.data['data']['profiles'] == created_openuser_2.profiles
        assert 'Deleted successfully' == res.data['data']['detail']
