from django.test import TestCase
from django.core.urlresolvers import resolve

from dictionary.views import search, word, gloss


class DictionaryURLs(TestCase):
    def test_root_url_resolves_to_search_view(self):
        '''
        '/' should be routed to the search function
        in 'views.py'
        '''
        found = resolve('/')
        self.assertEqual(found.func, search)

    def test_search_url_resolves_to_search_view(self):
        '''
        '/search/' should be routed to the search function
        in 'views.py'
        '''
        found = resolve('/search/')
        self.assertEqual(found.func, search)

    def test_word_url_resolves_to_word_view(self):
        '''
        '/words/jet-1/', for example, should be routed
        to the word view.
        '''
        found = resolve('/words/jet-1.html')
        self.assertEqual(found.func, word)

    def test_gloss_url_resolves_to_gloss_view(self):
        '''
        '/gloss/1/', for example, should be routed
        to the gloss view.
        '''
        found = resolve('/gloss/1.html')
        self.assertEqual(found.func, gloss)
