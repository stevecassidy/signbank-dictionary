from django.conf.urls import include, url

from .dummy_view import dummy


feedback_urls = [
    # ex: generalfeedback/
    url(r"^generalfeedback/$", dummy,
        name="generalfeedback"),
    # ex: missingsign/
    url(r'^missingsign/$', dummy,
        name='missingsign'),
    # ex: sign/abscond-1/
    url(r'^word/(?P<keyword>.+)-(?P<n>\d+)/$', dummy,
        name = 'wordfeedback'),
    # ex: gloss/1
    url(r'^gloss/(?P<n>\d+)/$', dummy,
        name = 'glossfeedback')
]


video_urls = [
    url(r'^video/(?P<videoid>\d+)/$', dummy, name='video'),
    # ex: upload/
    url(r'^upload/$', dummy, name="add_video"),
    # ex: delete/1/
    url(r'^delete/(?P<videoid>\d+)/$', dummy, name='delete'),
    # ex: poster/1/
    url(r'^poster/(?P<videoid>\d+)/$', dummy, name='poster'),
    url(r'^iframe/(?P<videoid>\d+)/$', dummy, name='iframe'),
    ]


urlpatterns = [
    url(r"^", include("dictionary.urls", namespace="dictionary")),
    url(r"^feedback/", include(feedback_urls, namespace="feedback")),
    url(r"^video/", include(video_urls, namespace="video")),
]
