import pytest
from fastapi import FastAPI
from mongoengine import Document, connect, fields

from fastapi_pagination import LimitOffsetPage, Page, add_pagination
from fastapi_pagination.ext.mongoengine import paginate
from tests.base import BasePaginationTestCase

from .utils import mongodb_test


@pytest.fixture(scope="session")
def db_connect(database_url):
    connect(host=database_url)


@pytest.fixture(scope="session")
def user(db_connect):
    class User(Document):
        name = fields.StringField()

        meta = {
            "collection": "users",
            "strict": False,
            "id_field": "id",
        }

    return User


@pytest.fixture(
    scope="session",
    params=[True, False],
    ids=["model", "query"],
)
def query(request, user):
    if request.param:
        return user

    return user.objects.all()


@pytest.fixture(scope="session")
def app(db_connect, query, model_cls):
    app = FastAPI()

    @app.get("/default", response_model=Page[model_cls])
    @app.get("/limit-offset", response_model=LimitOffsetPage[model_cls])
    def route():
        return paginate(query)

    return add_pagination(app)


@mongodb_test
class TestMongoEngine(BasePaginationTestCase):
    pass
