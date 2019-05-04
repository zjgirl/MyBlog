#!/usr/bin/env python


from app import create_app, db #__init__ make a folder package
from app.model import *
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager, Shell


app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Post=Post, Role=Role, Follow=Follow, Permission=Permission)

# this make 'Permission' can be used in Jinja
@app.context_processor
def make_context():
    return dict(Permission=Permission)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand) #add command 'db'


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        manager.run()


