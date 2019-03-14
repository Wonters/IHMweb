from __future__ import absolute_import, unicode_literals

from celery import Celery

appTestcase = Celery('testcase',
                     broker='amqp://',
                     backend='amqp://',
                     include=['test_bench.tasks'])

# Optional configuration, see the application user guide.
appTestcase.conf.update(result_expires=3600, )

if __name__ == '__main__':
    appTestcase.start()
