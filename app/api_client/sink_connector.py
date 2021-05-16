from apiclient import APIClient


class ApiConnectorError(Exception):
    def __init__(self, type, message, response=None):
        self.type = type
        self.message = message
        self.response = response

    def __str__(self):
        return "%s (%s)" % (self.type, self.message)

    def __repr__(self):
        return "%s(type=%s)" % (self.__class__.__name__, self.type)


class ApiConnector(APIClient):
    BASE_URL = 'http://connect:8083/'

    def _handle_response(self, response):
        r = super(ApiConnector, self)._handle_response(response)

        has_error = r.get('error')
        if not has_error:
            return r

        raise ApiConnectorError(has_error['type'], has_error['message'], response=response)


def api_call(contextpath, params):
    apiclient = ApiConnector()
    result = apiclient.call(contextpath, params)
    print(f"Api call made for contextpath and params - {contextpath}, -{params} and the result is - {result}")
    return result
