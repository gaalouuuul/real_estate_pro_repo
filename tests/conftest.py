import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from app import create_app
from app.config import TestConfig
from app.extensions import db


@pytest.fixture()
def app_instance():
    app = create_app(TestConfig)
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app_instance):
    return app_instance.test_client()
