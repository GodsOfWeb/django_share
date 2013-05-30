from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^fb/', 'django_share.views.facebook_connect'),
    url(r'^fb_answer/', 'django_share.views.fb_answer'),
    url(r'^post_fb/', 'django_share.views.post_fb'),
    url(r'^linkedin/', 'django_share.views.linkedin'),
)
