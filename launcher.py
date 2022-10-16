from flask_migrate import upgrade, Migrate

from app import create_app, db
import os

app = create_app(os.getenv('FLASK_CONFIG') or "default")
migrate = Migrate(app, db, render_as_batch=True)


@app.cli.command()
def deploy():
    """Prepare everything for a new deployment"""
    # migrate database to latest revision
    upgrade()
