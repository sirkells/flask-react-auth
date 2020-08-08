from flask.cli import FlaskGroup

from app import create_app, db
from app.api.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

# This registers a new command, recreate_db, to the CLI 
# so that we can run it from the command line, 
# which we'll use shortly to apply the model to the database.
@cli.command('recreate_db')
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    cli()