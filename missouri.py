# -*- coding:utf-8 -*-

import os
from app.common.util import print_skyblue
from app import create_app
from app import db
from flask_script import Manager
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

COV = None

if os.environ.get('MISSOURI_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app.*')
    COV.start()

if os.path.exists('.env'):
    print_skyblue('Importing environment from .env...')
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

app = create_app(os.getenv('MISSOURI_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    from livereload import Server
    app.debug = True
    live_server = Server(app=app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(host='0.0.0.0', port=9000)


@manager.command
def test(coverage=False):
    if coverage and not os.environ.get('MISSOURI_COVERAGE'):
        import sys
        os.environ['MISSOURI_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print_skyblue('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print_skyblue(
            'HTML version: file://{covdir}/index.html'.format(covdir=covdir))
        COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(
        app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
    app.run()


@manager.command
def deploy():
    from flask_migrate import upgrade
    from app.model.role import Role
    from app.model.user import User

    # upgrade database migrataion
    upgrade()
    # create roles
    Role.insert_roles()
    # make all users follow themselives.
    User.add_self_follows()


if __name__ == '__main__':
    try:
        manager.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
