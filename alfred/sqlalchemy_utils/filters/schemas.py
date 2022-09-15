from marshmallow import Schema, post_load

from .filters import Filter


class FilterSchema(Schema):
    def __init__(self, query):
        self.query = query
        super().__init__()

    def build_filter(self, filters_spec):
        sqlalchemy_filters_list = []

        for filter in filters_spec:
            filter_class = Filter(filter)
            sqlalchemy_formated = filter_class.format_for_sqlalchemy()
            sqlalchemy_filters_list.append(sqlalchemy_formated)

        return sqlalchemy_filters_list

    # ideal era existir um pre_load, é legal fazer aqui para
    # não depender de setup de schema
    def remove_skip_values(self, data):
        return {key: value for key, value in data.items() if value not in [None]}

    @post_load
    def make_object(self, data, **kwargs):
        clean_data = self.remove_skip_values(data)
        filters_spec = clean_data.values()
        sqlalchemy_filters = self.build_filter(filters_spec)
        self.filtered_query = self.query.filter(*sqlalchemy_filters)
        return self.query.filter(*sqlalchemy_filters)
