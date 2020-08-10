from flask.cli import FlaskGroup

from app import create_app, db
from app.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

# This registers a new command, recreate_db, seed_db, to the CLI 
# so that we can run it from the command line, 
# which we'll use shortly to apply the model to the database.
# >> python manage.py seed_db
# or
# >> docker-compose exec users python manage.py seed_db  
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    db.session.add(User(username='michael', email="hermanmu@gmail.com"))
    db.session.add(User(username='michaelherman', email="michael@mherman.org"))
    db.session.commit()

if __name__ == '__main__':
    cli()