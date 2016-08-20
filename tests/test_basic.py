from rest_client import RestClient

from pytest import fixture
import requests


class TestBasic:
    @fixture
    def base_url(self):
        return 'http://localhost'

    @fixture
    def base_url_slash(self):
        return 'http://localhost/'

    @fixture
    def url_client(self, base_url):
        return RestClient(base_url=base_url, urls_only=True)

    @fixture
    def url_client_slash(self, base_url_slash):
        return RestClient(base_url=base_url_slash, urls_only=True)

    @fixture
    def client(self, base_url):
        return RestClient(base_url=base_url)

    def test_client_urls(self, url_client):
        expected_list_url = 'http://localhost/books/'
        expected_retrieve_url = 'http://localhost/authors/1/'
        dumb_data = {}
        dumb_params = {"filter": "something"}
        assert url_client.books.list(params=dumb_params) == expected_list_url
        assert url_client.books.create(data=dumb_data) == expected_list_url
        assert url_client.authors.retrieve(key=1) == expected_retrieve_url
        assert url_client.authors.partial_update(key=1, data=dumb_data)\
            == expected_retrieve_url
        assert url_client.authors.update(key=1, data=dumb_data)\
            == expected_retrieve_url
        assert url_client.authors.destroy(key=1) == expected_retrieve_url

    def test_client_urls_with_different_base(self, url_client_slash):
        expected_list_url = 'http://localhost/books/'
        expected_retrieve_url = 'http://localhost/authors/1/'
        dumb_data = {}
        dumb_params = {"filter": "something"}
        assert url_client_slash.books.list(params=dumb_params) \
            == expected_list_url
        assert url_client_slash.books.create(data=dumb_data) \
            == expected_list_url
        assert url_client_slash.authors.retrieve(key=1) \
            == expected_retrieve_url
        assert url_client_slash.authors.partial_update(key=1, data=dumb_data)\
            == expected_retrieve_url
        assert url_client_slash.authors.update(key=1, data=dumb_data)\
            == expected_retrieve_url
        assert url_client_slash.authors.destroy(key=1) == expected_retrieve_url

    def test_client_list_without_query(self, mocker, client):
        mocker.patch('requests.get')
        client.books.list()
        requests.get.assert_called_once_with('http://localhost/books/')

    def test_client_list_with_query(self, mocker, client):
        mocker.patch('requests.get')
        dumb_params = {"filter": "something"}
        client.books.list(params=dumb_params)
        requests.get.assert_called_once_with('http://localhost/books/',
                                             params=dumb_params)

    def test_client_create(self, mocker, client):
        mocker.patch('requests.post')
        dumb_data = {"data": "something"}
        client.books.create(data=dumb_data)
        requests.post.assert_called_once_with('http://localhost/books/',
                                              data=dumb_data)

    def test_client_retrieve(self, mocker, client):
        mocker.patch('requests.get')
        client.books.retrieve(key=1)
        requests.get.assert_called_once_with('http://localhost/books/1/')

    def test_client_update(self, mocker, client):
        mocker.patch('requests.put')
        dumb_data = {"data": "something"}
        client.books.update(key=1, data=dumb_data)
        requests.put.assert_called_once_with('http://localhost/books/1/',
                                             data=dumb_data)

    def test_client_partial_update(self, mocker, client):
        mocker.patch('requests.patch')
        dumb_data = {"data": "something"}
        client.books.partial_update(key=1, data=dumb_data)
        requests.patch.assert_called_once_with('http://localhost/books/1/',
                                               data=dumb_data)

    def test_client_destroy(self, mocker, client):
        mocker.patch('requests.delete')
        client.books.destroy(key=1)
        requests.delete.assert_called_once_with('http://localhost/books/1/')
