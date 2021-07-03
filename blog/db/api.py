from oslo_config import cfg
from oslo_db import api as db_api
from oslo_db.sqlalchemy import session as db_session


_BACKEND_MAPPING = {
    'sqlalchemy': 'blog.db.sqlalchemy.api',
}

IMPL = db_api.DBAPI('sqlalchemy', backend_mapping=_BACKEND_MAPPING)


def _get_facade():
    global _FACADE
    if _FACADE is None:
        _FACADE = db_session.EngineFacade.from_config(cfg.CONF, sqlite_fk=True)
    return _FACADE


def get_session(expire_on_commit=False, autocommit=False):
    facade = _get_facade()
    return facade.get_session(expire_on_commit=expire_on_commit,
                              autocommit=autocommit)


def get_engine():
    facade = _get_facade()
    return facade.get_engine()


def setup_db():
    IMPL.setup_db()


def model_query(model, columns=()):
    session = get_session()

    if columns:
        return session.query(*columns)

    return session.query(model)


def get_post(id):
    return IMPL.get_post(id)


def get_posts():
    return IMPL.get_posts()


def create_post(title, content):
    return IMPL.create_post(title, content)


def delete_post(id):
    return IMPL.delete_post(id)