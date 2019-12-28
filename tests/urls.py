from django.urls import include, path

from .dummy_view import dummy

feedback_urls = [
    # ex: generalfeedback/
    path("generalfeedback/", dummy, name="generalfeedback"),
    # ex: missingsign/
    path('missingsign/', dummy, name='missingsign'),
    # ex: sign/abscond-1/
    path('word/<keyword>-<int:n>/', dummy, name = 'wordfeedback'),
    # ex: gloss/1
    path('gloss/<int:n>/', dummy, name = 'glossfeedback')
]


video_urls = [
    path('video/<int:videoid>/', dummy, name='video'),
    # ex: upload/
    path('upload/', dummy, name="add_video"),
    # ex: delete/1/
    path('delete/<int:videoid>/', dummy, name='delete'),
    # ex: poster/1/
    path('poster/<int:videoid>/', dummy, name='poster'),
    path('iframe/<int:videoid>/', dummy, name='iframe'),
    ]


urlpatterns = [
    path("", include("dictionary.urls", namespace="dictionary")),
    path("feedback/", include((feedback_urls, 'feedback'), namespace="feedback")),
    path("video/", include((video_urls, 'video'), namespace="video")),
]
