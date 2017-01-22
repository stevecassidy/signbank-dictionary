# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory, override_settings
from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import AnonymousUser, User, Permission
from tagging.models import Tag
from django.http import Http404
from django.db.models import Max
from django.contrib.auth.decorators import login_required, permission_required

from dictionary.adminviews import GlossListView, GlossDetailView, gloss_ajax_complete
from dictionary.models import Keyword, Gloss


def create_request(url=None, method='GET', data=None, permission=None, logged_in=True):
    '''
    This function returns one of various kinds of requests. The kind
    of request that this function returns depends on the parametres
    passed to function.

    Call this function in a test case and then use the returned
    request as an argument to a view.
    '''
    factory = RequestFactory()
    # Set up the user...
    if logged_in:
        user = create_user(permission)
    else:
        user = AnonymousUser()
    if 'GET' in method.upper():
        request = factory.get(url, data)
    elif 'POST' in method.upper():
        request = factory.post(url, data)
    else:
        raise ValueError("%s is an unrecognised method. It must be one of 'post' or 'get'"%(method))
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    request.user = user
    return request


def create_user(permission=None):
    users = User.objects.all()
    nusers = len(users)
    # If a user doesn't exist already...
    if nusers != 1:
        user = User.objects.create_user(
            username='Jacob', email='jacob@…', password='top_secret', first_name = "Jacob",
            last_name = "smith")
    else:
        # If the user has already been created, use it
        user = users[0]
    if permission is not None:
        permission = Permission.objects.get(name=permission)
        user.user_permissions.add(permission)
    return user

class TestGlossListView(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        # An idgloss that exists in the fixture...
        self.login_url = '/accounts/login/?next=/None'
        self.view = permission_required('dictionary.search_gloss')(GlossListView.as_view())

    def test_not_logged_in(self):
        '''
        A user who is not logged in should
        be sent to the login page
        if he requests the glosslist view.
        '''
        request = create_request(logged_in = False)
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    def test_logged_in_but_not_admin(self):
        '''
        A user who is not an admin should not be
        able to see the page, should get a redirect to login.

        '''
        request = create_request(logged_in = True)
        response = self.view(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)
