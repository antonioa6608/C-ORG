import os
import pytest
import tempfile
from mechanic_site import create_app
from mechanic_site.db import init_db

@pytest.fixture
def app():
    # Create a temporary database file and initialize the app with it
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.app_context():
        init_db()

    yield app

    # Close and remove the temporary database file after testing
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()