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

    # create uploads directory
    upload_dir = os.path.join(app.root_path, app.config['UPLOAD_PATH'])
    os.makedirs(upload_dir, exist_ok=True)
