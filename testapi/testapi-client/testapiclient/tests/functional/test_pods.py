import unittest
from mock import mock
from testapiclient.pods import PodGet
from testapiclient.pods import PodGetOne
from testapiclient.pods import PodCreate
from testapiclient.pods import PodDelete
import argparse
import StringIO


class PodTest(unittest.TestCase):

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get(self, pod_get_http_mock):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(name='dfs')
        pod_get.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with('http://localhost:8000/api/v1/pods?name=dfs')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get_all(self, pod_get_http_mock):
        pod_get = PodGet(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(name='')
        pod_get.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with('http://localhost:8000/api/v1/pods')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_get_one(self, pod_get_http_mock):
        pod_get_one = PodGetOne(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(name='def')
        pod_get_one.take_action(parsed_args)
        pod_get_http_mock.get_Instance().get.assert_called_once_with('http://localhost:8000/api/v1/pods/def')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create(self, pod_create_http_mock):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(u='', p='', pod='{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_called_once_with('http://localhost:8000/api/v1/pods', None, '{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_success(self, pod_create_http_mock):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            pod_create_http_mock.get_Instance().post.return_value.status_code = 200
            parsed_args = argparse.Namespace(u='', p='', pod='{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')
            pod_create.take_action(parsed_args)
            self.assertEqual(mock_stdout.getvalue(), "Pod has been successfully created!\n")

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_failure(self, pod_create_http_mock):
        with mock.patch('sys.stdout', new=StringIO.StringIO()) as mock_stdout:
            pod_create = PodCreate(mock.Mock(), mock.Mock())
            pod_create_http_mock.get_Instance().post.return_value.status_code = 400
            pod_create_http_mock.get_Instance().post.return_value.text = "Error"
            parsed_args = argparse.Namespace(u='', p='', pod='{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')
            pod_create.take_action(parsed_args)
            self.assertEqual(mock_stdout.getvalue(), "Error\n")

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_unauthorized(self, pod_create_http_mock, pod_auth):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        pod_auth.authenticate.return_value.text = 'login'
        parsed_args = argparse.Namespace(u='user', p='password', pod='{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_not_called()

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_create_authorized(self, pod_create_http_mock, pod_auth):
        pod_create = PodCreate(mock.Mock(), mock.Mock())
        pod_auth.authenticate.return_value.text = 'success'
        parsed_args = argparse.Namespace(u='user', p='password', pod='{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')
        pod_create.take_action(parsed_args)
        pod_create_http_mock.get_Instance().post.assert_called_once_with('http://localhost:8000/api/v1/pods', None, '{ "role": "community-ci", "name": "", "details": "", "mode": "metal"}')

    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete(self, pod_delete_http_mock):
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(u='', p='', name='def')
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_called_once_with('http://localhost:8000/api/v1/pods/def', None)

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete_unauthorized(self, pod_delete_http_mock, pod_auth):
        pod_auth.authenticate.return_value.text = 'login'
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(u='user', p='pass', name='def')
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_not_called()

    @mock.patch('testapiclient.pods.AuthHandler')
    @mock.patch('testapiclient.pods.HTTPClient')
    def test_delete_authorized(self, pod_delete_http_mock, pod_auth):
        pod_auth.authenticate.return_value.text = 'success'
        pod_delete = PodDelete(mock.Mock(), mock.Mock())
        parsed_args = argparse.Namespace(u='user', p='pass', name='def')
        pod_delete.take_action(parsed_args)
        pod_delete_http_mock.get_Instance().delete.assert_called_once_with('http://localhost:8000/api/v1/pods/def', None)
