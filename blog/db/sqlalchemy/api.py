import sys
import threading

from oslo_db import exception as oslo_db_exc
from oslo_db.sqlalchemy import utils as db_utils
import sqlalchemy as sa

from blog.db import api as db_api
from blog.db.sqlalchemy import models


_SCHEMA_LOCK = threading.RLock()
_initialized = False


def get_backend():
    return sys.modules[__name__]


def setup_db():
    global _initialized

    with _SCHEMA_LOCK:
        if _initialized:
            return

        try:
            models.Post.metadata.create_all(db_api.get_engine())
            _initialized = True
        except sa.exc.OperationalError as e:
            raise Exception("Failed to setup database: %s" % str(e))


def _paginate_query(model, limit=None, marker=None, sort_keys=None,
                    sort_dirs=None, query=None):
    sort_keys = sort_keys if sort_keys else []

    if 'id' not in sort_keys:
        sort_keys.append('id')
        sort_dirs.append('asc') if sort_dirs else None

    query = db_utils.paginate_query(
        query,
        model,
        limit,
        sort_keys,
        marker=marker,
        sort_dirs=sort_dirs
    )

    return query


def _get_collection(model, limit=None, marker=None, sort_keys=None, sort_dirs=None):
    query = db_api.model_query(model)
    query = _paginate_query(
        model,
        limit,
        marker,
        sort_keys,
        sort_dirs,
        query
    )

    try:
        return query.all()
    except Exception as e:
        raise Exception(
            "Failed when querying database, error type: %s, "
            "error message: %s" % (e.__class__.__name__, str(e))
        )


def _get_collection_sorted_by_time(model, sort_keys=['created_at'], **kwargs):
    return _get_collection(
        model=model,
        sort_keys=sort_keys,
        **kwargs
    )


def _get_db_object_by_id(model, id):
    query = db_api.model_query(model)
    return query.filter_by(id=id).first()


def get_post(id):
    post = _get_db_object_by_id(models.Post, id)

    if not post:
        raise Exception("Post not found [id=%s]" % id)

    return post


def get_posts():
    return _get_collection_sorted_by_time(models.Post, sort_keys=['created'])


def create_post(title, content):
    session = db_api.get_session()
    post = models.Post()
    post.update({'title': str(title), 'content': str(content)})
    try:
        post.save(session=session)
    except oslo_db_exc.DBDuplicateEntry as e:
        raise Exception(
            "Duplicate entry for Post: %s" % e.columns
        )

    return post


def update_post(id, title, content):
    post = _get_db_object_by_id(models.Post, id)
    post.update({'title': title, 'content': content})
    return post


def delete_post(id):
    session = db_api.get_session()
    post = get_post(id)
    session.delete(post)
    session.flush()