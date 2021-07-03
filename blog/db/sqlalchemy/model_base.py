from oslo_db.sqlalchemy import models as oslo_models
from oslo_utils import uuidutils
import sqlalchemy as sa
from sqlalchemy.ext import declarative


def id_column():
    return sa.Column(
        sa.String(36),
        primary_key=True,
        default=uuidutils.generate_uuid
    )


def datetime_to_str(dct, attr_name):
    """Convert datetime object in dict to string."""
    if (dct.get(attr_name) is not None and
            not isinstance(dct.get(attr_name), six.string_types)):
        dct[attr_name] = dct[attr_name].strftime('%Y-%m-%dT%H:%M:%SZ')


class _ModelBase(oslo_models.ModelBase):
    """Base class for all SQLAlchemy DB Models."""

    __table__ = None

    __hash__ = object.__hash__

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False

        for col in self.__table__.columns:
            # In case of single table inheritance a class attribute
            # corresponding to a table column may not exist so we need
            # to skip these attributes.
            if (hasattr(self, col.name) and hasattr(other, col.name) and
                    getattr(self, col.name) != getattr(other, col.name)):
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        """sqlalchemy based automatic to_dict method."""
        d = {}

        for col in self.__table__.columns:
            d[col.name] = getattr(self, col.name)

        datetime_to_str(d, 'created')

        return d

    def __repr__(self):
        return '%s %s' % (type(self).__name__, self.to_dict().__repr__())


ModelBase = declarative.declarative_base(cls=_ModelBase)