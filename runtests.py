#!/usr/bin/env python

import os, sys
from django.conf import settings

DIRNAME = os.path.dirname(os.path.abspath(__file__))
settings.configure(DEBUG=True,
                   DATABASES={
                        'default': {
                            'ENGINE': 'django.db.backends.sqlite3',
                        }
                    },
                   TEMPLATE_DIRS=(os.path.join(DIRNAME, "registration_links/tests/templates"),),
                   ROOT_URLCONF='registration_links.tests.urls',
                   INSTALLED_APPS=('django.contrib.auth',
                                  'django.contrib.contenttypes',
                                  'django.contrib.sessions',
                                  'django.contrib.admin',
                                  'registration',
                                  'registration_links'))

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['registration_links', ])
if failures:
    sys.exit(failures)
