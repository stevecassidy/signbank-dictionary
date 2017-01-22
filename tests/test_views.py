# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory, override_settings
from django.conf import settings
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import AnonymousUser, User, Permission
from tagging.models import Tag
from django.http import Http404
from django.db.models import Max

from dictionary.views import (search, remove_crude_words,
    remove_words_not_belonging_to_category, paginate, word,
    get_gloss_position, gloss)
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


class SearchView(TestCase):
    # Django will populate the database with the data
    # in the file 'test_data.json'.
    # You should read the django docs to understand how this works.
    fixtures = ["test_data.json"]

    def setUp(self):
        self.login_url = '/accounts/login/?next=/None'

    def test_search_view_no_get_variables(self):
        '''
        The 'search' view should render
        'search_result.html' and
        it should return a response code of 200
        when no get variables are passed.
        '''
        request=create_request(method='get')
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request)
        self.assertEqual(response.status_code, 200)

    @override_settings(ALWAYS_REQUIRE_LOGIN=True)
    def test_not_logged_in_and_login_required(self):
        '''
        A user who is not logged in should
        be sent to the login page
        if he requests the search view.
        '''
        request = create_request(logged_in = False)
        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    @override_settings(ALWAYS_REQUIRE_LOGIN=False)
    def test_not_logged_in_and_login_not_required(self):
        '''
        A user who is not logged in should
        not be sent to the login page
        if he requests the search view.
        '''
        request = create_request(logged_in = False)
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request)
        self.assertEqual(response.status_code, 200)

    def test_remove_crude_words(self):
        '''
        'remove_curde_words' in views.py
        should remove all keywords that are
        tagged 'lexis:crude'.
        '''
        words = Keyword.objects.all()
        # There are nunfiltered keywords in the database
        nunfiltered = len(words)
        # let's add a crude tag to the first gloss of the first keyword...
        bad_word = words[0]
        bad_gloss = bad_word.translation_set.all()[0].gloss
        Tag.objects.update_tags(bad_gloss, 'lexis:crude')
        # Let's now filter
        filtered_words = remove_crude_words(words)
        self.assertEqual(nunfiltered-1, len(filtered_words))
        self.assertNotIn(bad_word, filtered_words)

    def test_remove_words_not_belonging_to_category(self):
        '''
        Words not belonging to the category
        'semantic:health' should be removed
        by the function '
        remove_words_not_belonging_to_category'
        '''
        words = Keyword.objects.all()
        # There are nunfiltered keywords in the database
        nunfiltered = len(words)
        # let's add a health tag to the first gloss of the first keyword...
        health_word = words[0]
        health_gloss = health_word.translation_set.all()[0].gloss
        category = 'semantic:health'
        Tag.objects.update_tags(health_gloss, category)
        # Let's now filter
        filtered_words = remove_words_not_belonging_to_category(words, category)
        self.assertEqual(1, len(filtered_words))
        self.assertIn(health_word, filtered_words)

    def test_search_view_keyword_as_get_variable_no_matches(self):
        '''
        passing a keyeword that matches nothing should
        render the template 'dictionary/search_result.html'
        ,and should return a response code of 200.
        '''
        request=create_request(method='get', data={'query':'✝'})
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request)
        self.assertEqual(response.status_code, 200)

    def test_search_view_keyword_as_get_variable_1_exact_match(self):
        '''
        passing a keyeword that exactly matches only 1 keyword should
        redirect to the keyword's gloss page.
        '''
        data={'query':'Aborigine'}
        request=create_request(method='get', data=data)
        response = search(request)
        self.assertEqual(response.status_code, 302)
        redirect_url = '/dictionary/words/%s-1'%data['query']
        self.assertTrue(response.url, redirect_url)

    def test_search_view_keyword_as_get_variable_inexact_match(self):
        '''
        passing a keyeword that inexactly matches a keyword should
        render the template 'dictionary/search_result.html'
        ,and should return a response code of 200.
        '''
        request=create_request(method='get', data={'query':'Aborigin'})
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request)
        self.assertEqual(response.status_code, 200)


class TestHelperMethods(TestCase):
    '''
    This class tests functions in views.py
    that are not views.
    '''
    fixtures = ["test_data.json"]

    def test_paginate_page_not_an_integer(self):
        '''
        Paginate should return the 1st page of objects
        if the requested page number is not a valid number.
        '''
        # j is not a valid number
        data = {'page' : 'j'}
        request = create_request(method='get', data=data)
        npages = 50
        # create 100 objects
        objects = ['a' for i in range(0,100)]
        (result_page, paginator) = paginate(request, objects ,npages)
        self.assertEqual(result_page.number,1)

    def test_painate_page_out_of_range(self):
        '''
        Paginate should return the last page of objects
        if the requested page number is out of range.
        '''
        # 3 will be out of range, because there will be only 2 pages
        data = {'page' : 3}
        request = create_request(method='get', data=data)
        # page is not a valid number
        npages = 50
        # create 100 objects
        objects = ['a' for i in range(0,100)]
        (result_page, paginator) = paginate(request, objects ,npages)
        self.assertEqual(result_page.number, 2)

    def test_paginate_no_page_number_requested(self):
        '''
        Paginate should return the first page if
        no page number is requested.
        '''
        request = create_request(method='get')
        # page is not a valid number
        npages = 50
        # create 100 objects
        objects = ['a' for i in range(0,100)]
        (result_page, paginator) = paginate(request, objects ,npages)
        self.assertEqual(result_page.number, 1)

    def test_paginate_no_page_number_requested(self):
        '''
        Paginate should return the first page if
        the list of objects is empty.
        '''
        request = create_request(method='get')
        # page is not a valid number
        npages = 50
        # create 0 objects
        objects = []
        (result_page, paginator) = paginate(request, objects ,npages)
        self.assertEqual(result_page.number, 1)

    def test_get_gloss_position_first_gloss(self):
        '''
        get_gloss_position should return the right position of
        the passed in gloss relative to the other glosses.

        Also, the gloss being tested has an sn of 1, so this is an edge case...
        '''
        # Let's use the first gloss...
        gloss = Gloss.objects.get(sn=1)
        # How many glosses are there?
        nglosses = len(Gloss.objects.all())
        can_view_gloss_not_inWeb = True
        (glossposn, glosscount) = get_gloss_position(gloss,
            can_view_gloss_not_inWeb)
        self.assertEqual(glossposn, gloss.sn)
        self.assertEqual(glosscount, nglosses)

    def test_get_gloss_position_last_gloss(self):
        '''
        get_gloss_position should return the right position of
        the passed in gloss relative to the other glosses.

        Also, the gloss being tested has an sn of max(Gloss.sn),
        so this is an edge case...
        '''
        # Let's get the last gloss...
        last_sn = Gloss.objects.all().aggregate(Max('sn'))['sn__max']
        gloss = Gloss.objects.get(sn=last_sn)
        # How many glosses are there?
        nglosses = len(Gloss.objects.all())
        can_view_gloss_not_inWeb = True
        (glossposn, glosscount) = get_gloss_position(gloss,
                can_view_gloss_not_inWeb)
        # Its position is nglosses, not neccessarily its sn.
        self.assertEqual(glossposn, nglosses)
        self.assertEqual(glosscount, nglosses)

    def test_get_gloss_position_gap(self):
        '''
        gloss a has sn of 1, and gloss b has sn of 3. Then
        gloss b has a position of 2, not 3...
        '''
        # Let's use the first gloss...
        gloss = Gloss.objects.get(sn=3)
        # How many glosses are there?
        nglosses = len(Gloss.objects.all())
        can_view_gloss_not_inWeb = True
        (glossposn, glosscount) = get_gloss_position(gloss,
                can_view_gloss_not_inWeb)
        # It should have a position of 2...
        self.assertEqual(glossposn, 2)
        self.assertEqual(glosscount, nglosses)

class WordView(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        # A keyword that exists in the fixture
        self.keyword = 'Aborigine'
        self.n = 1

    def test_word_view_return_200_response_code_and_right_template(self):
        '''
        The 'word' view should render
        'word.html' and
        it should return a response code of 200.
        '''
        request=create_request(method='get')
        with self.assertTemplateUsed('dictionary/word.html'):
                response = word(request, self.keyword, self.n)
        self.assertEqual(response.status_code, 200)

    def test_word_view_returns_404_for_non_existent_keyword(self):
        '''
        'word' should return a 404 if the keyword passed to it
        doesn't exist.
        '''
        request=create_request(method='get')
        non_existent_keyword = 'zzzzazer'
        self.assertRaises(Http404, word, request, non_existent_keyword, self.n)

    def test_word_view_returns_404_if_gloss_not_inWeb_and_not_admin(self):
        '''
        If you're not an admin and you try to view a keyword for which
        no gloss is inWeb, then you should get 404.
        '''
        keyword_whose_gloss_not_inWeb = 'Abraham'
        request=create_request(method='get')
        self.assertRaises(Http404, word, request, keyword_whose_gloss_not_inWeb,
            self.n)

    def test_inWeb_irrelevant_when_admin(self):
        '''
        If you're  an admin and you try to view a keyword for which
        no gloss is inWeb, then you should get 200 response code
        and right template.
        '''
        keyword_whose_gloss_not_inWeb = 'Abraham'
        permission = 'Can Search/View Full Gloss Details'
        request=create_request(method='get', permission=permission)
        with self.assertTemplateUsed('dictionary/word.html'):
                response = word(request, keyword_whose_gloss_not_inWeb, self.n)
        self.assertEqual(response.status_code, 200)


    def test_admin_sees_detail_button(self):
        '''
        If you're  an admin then you see a button linking
        to Detail View on a word page.
        '''
        keyword_whose_gloss_not_inWeb = 'Abraham'
        permission = 'Can Search/View Full Gloss Details'
        request=create_request(method='get', permission=permission)
        with self.assertTemplateUsed('dictionary/word.html'):
                response = word(request, keyword_whose_gloss_not_inWeb, self.n)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Detail View')



class Glossview(TestCase):
    fixtures = ["test_data.json"]

    def setUp(self):
        # An idgloss that exists in the fixture...
        self.idgloss = 'Aborigine1'
        self.login_url = '/accounts/login/?next=/None'

    @override_settings(ALWAYS_REQUIRE_LOGIN=True)
    def test_not_logged_in_and_login_required(self):
        '''
        A user who is not logged in should
        be sent to the login page
        if he requests the gloss view.
        '''
        request = create_request(logged_in = False)
        response = gloss(request, self.idgloss)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)

    @override_settings(ALWAYS_REQUIRE_LOGIN=False)
    def test_not_logged_in_and_login_not_required(self):
        '''
        A user who is not logged in should
        not be sent to the login page
        if he requests the gloss view.
        '''
        request = create_request(logged_in = False)
        with self.assertTemplateUsed('dictionary/word.html'):
                response = gloss(request, self.idgloss)
        self.assertEqual(response.status_code, 200)

    def test_gloss_not_inWeb_and_user_not_admin(self):
        '''
        A user who is not an admin, but who
        tries to view a gloss that is not InWeb,
        should be denied; 404 should be returned.
        '''
        # Let's get a gloss that isn't inWeb
        gloss_not_inWeb = Gloss.objects.filter(inWeb=False)[0]
        request = create_request(method='get')
        self.assertRaises(Http404, gloss, request, gloss_not_inWeb.idgloss)

    def test_gloss_not_inWeb_irreleant_when_user_is_admin(self):
        '''
        A gloss not being inWeb shouldn't matter if the
        user is an admin; subsequently, the user should
        get a 200 response code and the right template...
        '''
        gloss_not_inWeb = Gloss.objects.filter(inWeb=False)[0]
        permission = 'Can Search/View Full Gloss Details'
        request=create_request(method='get', permission=permission)
        with self.assertTemplateUsed('dictionary/word.html'):
                response = gloss(request, gloss_not_inWeb.idgloss)
        self.assertEqual(response.status_code, 200)

    def test_gloss_does_not_exist(self):
        '''
        If a gloss that doesn't exist is passed to the
        gloss view, then 404 should be returned.
        '''
        non_existent_idgloss = 'ZZZ890'
        request = create_request()
        self.assertRaises(Http404, gloss, request, non_existent_idgloss)
