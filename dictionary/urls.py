from django.urls import path, re_path
from django.contrib.auth.decorators import login_required, permission_required
from .views import *
from .update import *
from .tagviews import *
from .adminviews import GlossListView, GlossDetailView, gloss_ajax_complete

app_name = 'dictionary'
urlpatterns = [

    # index page is just the search page
    path('', search),

    # we use the same view for a definition and for the feedback form on that
    # definition, the first component of the path is word or feedback in each case
    path('words/<keyword>-<int:n>.html', word, name='word'),

    path('tag/<tag>/', taglist, name='tag'),

    # and and alternate view for direct display of a gloss
    path('gloss/<idgloss>.html', gloss, name='gloss'),

    path('search/', search, name="search"),
    path('search/region/', set_region, name='set_region'),
    path('update/gloss/<int:glossid>', update_gloss, name='update_gloss'),
    path('update/tag/<int:glossid>', add_tag, name='add_tag'),
    path('update/definition/<int:glossid>', add_definition, name='add_definition'),
    path('update/relation/', add_relation, name='add_relation'),
    path('update/region/<int:glossid>', add_region, name='add_region'),
    path('update/gloss/', add_gloss, name='add_gloss'),

    path('ajax/keyword/<prefix>', keyword_value_list),
    path('ajax/tags/', taglist_json),
    path('ajax/gloss/<prefix>', gloss_ajax_complete, name='gloss_complete'),

    path('missingvideo.html', missing_video_view),

    path('variant/<idgloss>.html', variant, name='public_variant'),

    # Admin views
    path('list/', permission_required('dictionary.search_gloss')(GlossListView.as_view()), name='admin_gloss_list'),
    path('gloss/<int:pk>', permission_required('dictionary.search_gloss')(GlossDetailView.as_view()), name='admin_gloss_view'),

]
