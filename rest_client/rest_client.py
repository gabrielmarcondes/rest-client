import os
import requests


class InvalidParamsException(Exception):
    pass


class ResourceDriver:
    def __init__(self, resource_url, urls_only=False):
        self.resource_url = resource_url
        self.urls_only = urls_only

    def _base_resource_url(self):
        return "%s/" % (self.resource_url,)

    def _detail_resource_url(self, key):
        return os.path.join(self.resource_url, str(key), "")

    def list(self, params=None):
        url = self._base_resource_url()
        if self.urls_only:
            return url
        else:
            if params:
                return requests.get(url, params=params)
            else:
                return requests.get(url)

    def create(self, data=None):
        url = self._base_resource_url()
        if self.urls_only:
            return url
        else:
            return requests.post(url, data=data)

    def retrieve(self, key):
        url = self._detail_resource_url(key)
        if self.urls_only:
            return url
        else:
            return requests.get(url)

    def partial_update(self, key, data=None):
        url = self._detail_resource_url(key)
        if self.urls_only:
            return url
        else:
            return requests.patch(url, data=data)

    def update(self, key, data):
        url = self._detail_resource_url(key)
        if self.urls_only:
            return url
        else:
            return requests.put(url, data=data)

    def destroy(self, key):
        url = self._detail_resource_url(key)
        if self.urls_only:
            return url
        else:
            return requests.delete(url)


class RestClient:
    def __init__(self, base_url=None, urls_only=False):
        if not base_url:
            raise InvalidParamsException("base_url is mandatory")
        else:
            self.base_url = base_url
        self.urls_only = urls_only

    def _get_url(self, resource):
        return os.path.join(self.base_url, resource)

    def __getattr__(self, item):
        return ResourceDriver(self._get_url(item), urls_only=self.urls_only)
