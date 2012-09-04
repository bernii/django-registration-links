from django.conf.urls.defaults import patterns, url, include
from ..views import check_registration_link

urlpatterns = patterns('',
        url(r'^register/(?P<code>\w+)$', check_registration_link),
        url(r'^accounts/register/$', 'registration.views.register',
            {'backend': 'registration_links.SimpleBackend',
            'success_url': '/'},
            name='registration_register'),
        (r'^accounts/', include('registration.backends.simple.urls')),
    )
