import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

try:
    from django.conf import settings
    from django.test.utils import get_runner

    settings.configure(
        DEBUG=True,
        USE_TZ=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        ROOT_URLCONF="tests.urls",
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sites",
            'bootstrap3',
            "dictionary",
            "tagging",
            "video",
            "feedback"
        ],
        SITE_ID=1,

        FIXTURE_DIRS = [os.path.join(BASE_DIR, 'tests', 'fixtures')],

        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',

],

         TEMPLATES = [
          {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
                  'DIRS': [os.path.join((os.path.dirname(os.path.abspath(__file__))),
                            'tests', 'templates'),
            # insert your TEMPLATE_DIRS here
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
],
        LANGUAGE_NAME = 'Auslan',

        ALWAYS_REQUIRE_LOGIN = True,
        ANON_SAFE_SEARCH = False,
        QUICK_UPDATE_GLOSS_FIELDS = ['language', 'dialect'],
        VIDEO_UPLOAD_LOCATION = 'tmp',
        GLOSS_VIDEO_DIRECTORY = 'tmp',
        SHOW_TRADITIONAL = True,
        SHOW_FREQUENCY = True,
        ADMIN_RESULT_FIELDS = ['sn', 'idgloss', 'annotation_idgloss', 'morph'],

# which definition fields do we show and in what order?
DEFINITION_FIELDS = ['general', 'noun', 'verb', 'interact', 'diectic', 'modifier', 'question', 'augment', 'note'],
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
),
 # do we display the previous/next links to signs, requires gloss.sn to be used consistently
SIGN_NAVIGATION = True,
# settings for django-tagging
ANON_TAG_SEARCH = False,
FORCE_LOWERCASE_TAGS = True,
# a list of tags we're allowed to use
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
                 ],
                 )

    try:
        import django
        setup = django.setup
    except AttributeError:
        pass
    else:
        setup()


except ImportError:
    import traceback
    traceback.print_exc()
    msg = "To fix this error, run: pip install -r requirements_test.txt"
    raise ImportError(msg)


def run_tests(*test_args):
    if not test_args:
        test_args = ['tests']

    # Run tests
    TestRunner = get_runner(settings)
    test_runner = TestRunner()

    failures = test_runner.run_tests(test_args)

    if failures:
        sys.exit(bool(failures))


if __name__ == '__main__':
    run_tests(*sys.argv[1:])
