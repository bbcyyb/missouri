# -*- coding:utf-8 -*-

import os

COV = None

if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app.*')
    COV.start()

if os.path.exists('.env'):
    print 'Importing environment from .env...'
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]

from flask_script import Manager
from app import create_app, db
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def dev():
    pass


@manager.command
def test(coverage=False):
    pass


@manager.command
def profile(length=25, profile_dir=None):
    pass


@manager.command
def deploy():
    pass


if __name__ == '__main__':
    manager.run()
