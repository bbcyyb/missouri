# -*- coding:utf-8 -*-

import os
from app import create_app
from app import db
from flask_script import Manager
from flask_script import Server
from flask_migrate import Migrate
from flask_migrate import MigrateCommand

COV = None

if os.environ.get('MISSOURI_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app.*')
    COV.start()

if os.path.exists('.env'):
    print 'Importing environment from .env...'
    for line in open('.env'):
        var = line.strip().split('=')
        if len(var) == 2:
            os.environ[var[0]] = var[1]


app = create_app(os.getenv('MISSOURI_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0', port=9000))


@app.route('/yyb')
def test():
    print '=======>yyb'
    return '123'


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
    try:
        manager.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
