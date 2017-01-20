from django.conf.urls import *
from django.contrib.auth.decorators import login_required, permission_required
from .views import *
from .update import *
from .tagviews import *
from .adminviews import GlossListView, GlossDetailView, gloss_ajax_complete


urlpatterns = [

    # index page is just the search page
    url(r'^$', search),

    # we use the same view for a definition and for the feedback form on that
    # definition, the first component of the path is word or feedback in each case
    url(r'^words/(?P<keyword>.+)-(?P<n>\d+).html$', word, name='word'),

    url(r'^tag/(?P<tag>[^/]*)/?$', taglist, name='tag'),

    # and and alternate view for direct display of a gloss
    url(r'gloss/(?P<idgloss>.+).html$', gloss, name='gloss'),

    url(r'^search/$', search, name="search"),
    url(r'^update/gloss/(?P<glossid>\d+)$', update_gloss, name='update_gloss'),
    url(r'^update/tag/(?P<glossid>\d+)$', add_tag, name='add_tag'),
    url(r'^update/definition/(?P<glossid>\d+)$', add_definition, name='add_definition'),
    url(r'^update/relation/$', add_relation, name='add_relation'),
    url(r'^update/region/(?P<glossid>\d+)$', add_region, name='add_region'),
    url(r'^update/gloss/', add_gloss, name='add_gloss'),

    url(r'^ajax/keyword/(?P<prefix>.*)$', keyword_value_list),
    url(r'^ajax/tags/$', taglist_json),
    url(r'^ajax/gloss/(?P<prefix>.*)$', gloss_ajax_complete, name='gloss_complete'),

    url(r'^missingvideo.html$', missing_video_view),

    url(r'variant/(?P<idgloss>.+).html$', variant, name='public_variant'),

    # Admin views
    url(r'^list/$', permission_required('dictionary.search_gloss')(GlossListView.as_view()), name='admin_gloss_list'),
    url(r'^gloss/(?P<pk>\d+)', permission_required('dictionary.search_gloss')(GlossDetailView.as_view()), name='admin_gloss_view'),

]
