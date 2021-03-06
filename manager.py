import os.path
import imp

from app import app, db, models
from app.settings import Config
from migrate.versioning import api
from flask.ext.script import Manager, Shell, Server, Command

manager = Manager(app)
manager.add_command('runserver', Server(host='localhost'))
manager.add_command('shell', Shell())


@manager.command
def createdb():
    db.create_all()
    if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
        api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(Config.SQLALCHEMY_DATABASE_URI, 
                            Config.SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(Config.SQLALCHEMY_DATABASE_URI,
                            Config.SQLALCHEMY_MIGRATE_REPO,
                            api.version(Config.SQLALCHEMY_MIGRATE_REPO))

    print 'DB created'


@manager.command
def migratedb():
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                       Config.SQLALCHEMY_MIGRATE_REPO)
    migration = Config.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI,
                                 Config.SQLALCHEMY_MIGRATE_REPO)

    exec(old_model, tmp_module.__dict__)
    script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI,
                                              Config.SQLALCHEMY_MIGRATE_REPO,
                                              tmp_module.meta, db.metadata)

    open(migration, "wt").write(script)
    api.upgrade(Config.SQLALCHEMY_DATABASE_URI,
                Config.SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                       Config.SQLALCHEMY_MIGRATE_REPO)

    print 'New migration saved as ' + migration
    print 'Current database version: ' + str(v)


@manager.command
def upgraddb():
    api.upgrade(Config.SQLALCHEMY_DATABASE_URI,
                Config.SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                       Config.SQLALCHEMY_MIGRATE_REPO)
    print 'Current database version: ' + str(v)


@manager.command
def downgraddb():
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                       Config.SQLALCHEMY_MIGRATE_REPO)

    api.downgrade(Config.SQLALCHEMY_DATABASE_URI,
                  Config.SQLALCHEMY_MIGRATE_REPO, v - 1)
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI,
                       Config.SQLALCHEMY_MIGRATE_REPO)

    print 'Current database version: ' + str(v)

@manager.command
def import_dataset():
    from app import test_dataset

    for user in test_dataset.datasets:
        user_model = models.User(social_id=user['social_id'],
                    nickname=user['nickname'],
                    email=user['email'])
        db.session.add(user_model)
        db.session.commit()
  
        for word in user['words']:
            word_model = models.Word(name=word['name'],
                        explain=word['explain'],
                        example=word['example'],
                        created_at=word['created_at'],
                        updated_at=word['updated_at'],
                        user_id=user_model.id)
            db.session.add(word_model)
            db.session.commit()

    print 'Import ends'


if __name__ == "__main__":
    manager.run()
