import math

from chalice import Response as ChaliceResponse


class Response:
    """
    A class that represents the response for the view functions.
    It always returns a `chalice.Response`.
    """

    def __new__(
        self,
        status_code,
        body=None,
        headers=None,
        query=None,
        per_page=20,
        page=1,
        model_property="to_json",
    ):
        if body is not None:
            return self._simple_response(
                status_code=status_code, headers=headers, body=body
            )
        return self._query_response(
            status_code=status_code,
            headers=headers,
            query=query,
            per_page=per_page,
            page=page,
            model_property=model_property,
        )

    @classmethod
    def _query_response(
        self,
        status_code=None,
        headers=None,
        query=None,
        per_page=None,
        page=None,
        model_property=None,
    ):
        per_page = min(int(per_page), 100)

        page = int(page)
        total = query.count()
        total_pages = math.ceil(total / per_page)

        data = query.limit(per_page).offset((page - 1) * per_page).all()

        body = {
            "data": [instance.__getattribute__(model_property) for instance in data],
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": total_pages,
        }

        return ChaliceResponse(status_code=status_code, body=body, headers=headers)

    @classmethod
    def _simple_response(self, status_code=None, headers=None, body=None):
        return ChaliceResponse(status_code=status_code, body=body, headers=headers)
