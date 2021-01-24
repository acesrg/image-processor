import os

from flask_migrate import Migrate, MigrateCommand  # noqa: F401
from flask_script import Manager
from app import blueprint

from app.main import create_app

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app)


@manager.command
def run():
    app.run()


if __name__ == '__main__':
    manager.run()
