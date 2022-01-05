from datetime import datetime

from pynamodb.attributes import (
    JSONAttribute,
    ListAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.exceptions import DoesNotExist
from pynamodb.models import Model

from alfred.settings import DYNAMO_PREFIX


class BasicAuthUser(Model):
    class Meta:
        table_name = f"{DYNAMO_PREFIX}_basicauth_user"

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

        try:
            user = self.get(username)
            routes = user.routes if user.password == password else []
        except DoesNotExist:
            pass
        return routes
