import os
import sys
import pytest

# Add project root (part2) to PYTHONPATH so "hbnb" package is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from hbnb.app import create_app
from hbnb.app.models.user import User


@pytest.fixture()
def client():
    User._reset_used_emails()

    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as c:
        yield c