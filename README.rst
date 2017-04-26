=============================
signbank-dictionary
=============================

.. image:: https://badge.fury.io/py/signbank-dictionary.png
    :target: https://badge.fury.io/py/signbank-dictionary

.. image:: https://travis-ci.org/stevecassidy/signbank-dictionary.png?branch=master
    :target: https://travis-ci.org/stevecassidy/signbank-dictionary

.. image:: https://codecov.io/gh/stevecassidy/signbank-dictionary/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/stevecassidy/signbank-dictionary

The dictionary component of Signbank

Documentation
-------------

The full documentation is at https://signbank-dictionary.readthedocs.org.

Quickstart
----------

Install signbank-dictionary::

    pip install signbank-dictionary

Then use it in a project::

    import dictionary

You must define the following variables in ``settings.py``:

* ::

    DEFINITION_FIELDS = ['general', 'noun', 'verb', 'interact', 'diectic', 'modifier', 'question', 'augment', 'note']
* ::

    DEFINITION_ROLE_CHOICES = (('general', 'General Definition'),
    ('noun', 'As a Noun'),
    ('verb', 'As a Verb or Adjective'),
    ('deictic', 'As a Pointing Sign'),
    ('interact', 'Interactive'),
    ('modifier', 'As Modifier'),
    ('question', 'As Question'),
    ('popexplain', 'Popular Explanation'),
    ('augment', 'Augmented Meaning'),
    ('note', 'Note'),
    ('privatenote', 'Private Note'),
    ('B92 sn', 'Sign Number in Brien 92'),
    )

Those two variables configure how the definitions of signs are displayed in
the dictionary.

* ``ANON_TAG_SEARCH = True``
* ``ANON_SAFE_SEARCH = False``

These two variables specify whether an anonymous user (a user who is not
logged in) may search for a sign by tag, and whether signs categorised
as crude (offensive) will be filtered out of the search results for an
anonymous user, respectively.


* ``ALWAYS_REQUIRE_LOGIN = False``

This variable controls whether a user must be logged in
to search for signs.


* ``LANGUAGE_NAME  = 'Auslan'``

This variable specifies the sign language of the site.

* ``SIGN_NAVIGATION = True``
This variable specifies whether a navigation bar
in the dictionary is displayed. The navigation bar
allows a user to go from the sign whose entry he is currently
looking at to the next, or previous, sign in the sequence of signs.


* ``FORCE_LOWERCASE_TAGS = True``
* ::

    ALLOWED_TAGS = [ '',
                 'b92:directional',
                 'b92:regional',
                 'corpus:attested',
                 'iconicity:obscure',
                 'iconicity:opaque',
                 'iconicity:translucent',
                 'iconicity:transparent',
                 'lexis:battinson',
                 'lexis:classifier',
                 'lexis:crude',
                 'lexis:doubtlex',
                 'lexis:fingerspell',
                 'lexis:gensign',
                 'lexis:marginal',
                 'lexis:obsolete',
                 'lexis:proper name',
                 'lexis:regional',
                 'lexis:restricted lexeme',
                 'lexis:signed english',
                 'lexis:signed english only',
                 'lexis:technical',
                 'lexis:varlex',
                 'morph:begin directional sign',
                 'morph:body locating',
                 'morph:directional sign',
                 'morph:end directional sign',
                 'morph:locational and directional',
                 'morph:orientating sign',
                 'phonology:alternating',
                 'phonology:dominant hand only',
                 'phonology:double handed',
                 'phonology:forearm rotation',
                 'phonology:handshape change',
                 'phonology:onehand',
                 'phonology:parallel',
                 'phonology:symmetrical',
                 'phonology:two handed',
                 'religion:anglican',
                 'religion:catholic',
                 'religion:catholic school',
                 'religion:jehovas witness',
                 'religion:other',
                 'religion:religion',
                 'semantic:animal',
                 'semantic:arithmetic',
                 'semantic:arts',
                 'semantic:bodypart',
                 'semantic:car',
                 'semantic:city',
                 'semantic:clothing',
                 'semantic:color',
                 'semantic:cooking',
                 'semantic:day',
                 'semantic:deaf',
                 'semantic:drink',
                 'semantic:education',
                 'semantic:family',
                 'semantic:feel',
                 'semantic:food',
                 'semantic:furniture',
                 'semantic:government',
                 'semantic:groom',
                 'semantic:health',
                 'semantic:judge',
                 'semantic:language act',
                 'semantic:law',
                 'semantic:material',
                 'semantic:metalg',
                 'semantic:mind',
                 'semantic:money',
                 'semantic:nature',
                 'semantic:number',
                 'semantic:order',
                 'semantic:people',
                 'semantic:physical act',
                 'semantic:quality',
                 'semantic:quantity',
                 'semantic:question',
                 'semantic:recreation',
                 'semantic:rooms',
                 'semantic:salutation',
                 'semantic:sensing',
                 'semantic:sexuality',
                 'semantic:shapes',
                 'semantic:shopping',
                 'semantic:sport',
                 'semantic:telecommunications',
                 'semantic:time',
                 'semantic:travel',
                 'semantic:utensil',
                 'semantic:weather',
                 'semantic:work',
                 'school:state school',
                 'workflow:needs video',
                 'workflow:redo video',
                 'workflow:problematic',
                 ]
These two variables are used by the ``tagging`` app.
The ``tagging`` app is just a way of assigning categories to
signs.


You must also add ``dictionary``, and ``tagging`` to your ``INSTALLED_APPS`` variable.


Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
