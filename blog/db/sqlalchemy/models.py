from oslo_utils import timeutils
import sqlalchemy as sa

from blog.db.sqlalchemy import model_base as base


class Post(base.ModelBase):
    __tablename__ = 'posts'

    id = base.id_column()
    title = sa.Column(sa.String(255), nullable=False)
    content = sa.Column(sa.String(255), nullable=False)
    created = sa.Column(sa.DateTime, default=lambda: timeutils.utcnow())