from sqlalchemy import or_

from .operators import OPERATORS


class Filter(object):
    def __init__(self, filter):
        model_klass = filter["model"]
        self.sqlalchemy_field = getattr(model_klass, filter["field_name"])
        self.operator = OPERATORS[filter["op"]]
        self.value = filter["value"]
        self.filter_type = filter["filter_type"]

    def format_for_sqlalchemy(self):
        if self.filter_type == "sqlalchemy.or_":
            return or_(
                self.operator(self.sqlalchemy_field, item) for item in self.value
            )

        return self.operator(self.sqlalchemy_field, self.value)
