django-registration-links
=========================

A simple Django module for invite-only registration with unique access links. It is an additional helper module for [django-registration](http://bitbucket.org/ubernostrum/django-registration/)

Usage
-----

You have to define two urls in your *urls.py*.
 1. URL which will serve as the base for the custom registration codes (*register/* in the example)
 2. Custom registration backend for django-registration. It is used to block the registration if user is not using correct URL with code.

```python

urlpatterns = patterns('',
    # ...
    url(r'^register/(?P<code>\w+)$', 'registration_links.views.check_registration_link', name="check_registration_link"), # 1
    url(r'^accounts/register/$', 'registration.views.register', # 2
                           {'backend': 'registration_links.SimpleBackend', ...},
                           name='registration_register'),
	# ...
)

```

How it works
------------

Registration links can be created using *Django Admin* or in some automated manner that you can develop.

When user tries to visit registration page (/accounts/register/ when using same urls as in example) without using registration link, he is presented with 'registration closed' page. You can easily customize it by providing the template. It has to be placed in 'templates/registration/registration_closed.html'


Testing
-------

Project has full unit test coverage which you can run from your shell.

    ./manage.py test registration_links

![Continuous Integration status](https://secure.travis-ci.org/bernii/django-registration-links.png)

Got some questions or suggestions? [Mail me](mailto:bkobos+ghdrl@extensa.pl) directly or use the [issue tracker](/issues).