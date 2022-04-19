from datetime import datetime

from pynamodb.attributes import (
    JSONAttribute,
    ListAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.exceptions import DoesNotExist, GetError
from pynamodb.models import Model

from alfred.settings import DYNAMODB_HOST, DYNAMODB_PREFIX

from .exceptions import InvalidMetadataException, InvalidRoutesException


class BasicAuthUser(Model):
    class Meta:
        host = DYNAMODB_HOST
        table_name = f"{DYNAMODB_PREFIX}_basicauth_user"

    username = UnicodeAttribute(hash_key=True)
    password = UnicodeAttribute()
    routes = ListAttribute(null=True)
    created_at = UTCDateTimeAttribute(default=datetime.utcnow)
    metadata = JSONAttribute(null=True)

    @property
    def to_json(self):
        return {
            "username": self.username,
            "routes": self.routes,
            "created_at": str(self.created_at),
            "metadata": self.metadata,
        }

    @classmethod
    def login(self, username, password):
        routes = []
        if not username:
            return routes
        try:
            user = self.get(username)
            routes = user.routes if user.password == password else []
        except (DoesNotExist, GetError):
            pass
        return routes

    def add_routes(self, new_routes=[]):
        exit_conditions = (not new_routes, not isinstance(new_routes, list))
        if any(exit_conditions):
            raise InvalidRoutesException("New routes must be a valid list of routes")

        self.routes.extend(new_routes)
        self.save()

    def add_metadata(self, new_metadata={}):
        exit_conditions = (not new_metadata, not isinstance(new_metadata, dict))
        if any(exit_conditions):
            raise InvalidMetadataException("New metadata must be a valid dictionary")

        if self.metadata:
            self.metadata.update(new_metadata)
        else:
            self.metadata = new_metadata
        self.save()
