from six.moves.urllib import parse
import testtools

from testapiclient.client import scenarios
from testapiclient.tests.unit import fakes
from testapiclient.tests.unit import utils


class CustomClientTest(utils.TestCommand):
    def setUp(self):
        super(CustomClientTest, self).setUp()
        self.scenario_name = 'scenrio1'
        self.base_url = parse.urljoin(
            self.api_url,
            'scenarios/{}/customs'.format(self.scenario_name))
        self.custom_raw = 'custom'
        self.custom_input = ['custom']
        self.installer_name = 'installer'
        self.version_name = 'version'
        self.project_name = 'project'
        self.custom_client = scenarios.CustomsClient()


class CustomClientCreateTest(CustomClientTest):

    def setUp(self):
        super(CustomClientCreateTest, self).setUp()
        self.succ_rsp = {
            'href': '{}/{}'.format(
                self.base_url, self.scenario_name)
        }

    def test_create_success(self):
        self.post_mock.return_value = fakes.FakeResponse(
            data=self.succ_rsp)
        self.custom_client.create(
            self.scenario_name, self.installer_name,
            self.version_name, self.project_name,
            self.custom_raw)
        self.post_mock.assert_called_once()

    def test_create_failure(self):
        with testtools.ExpectedException(Exception, 'Create failed: Error'):
            self.post_mock.return_value = utils.FAKE_FAILURE
            self.custom_client.create(
                self.scenario_name, self.installer_name,
                self.version_name, self.project_name,
                self.custom_raw)


class CustomClientDeleteTest(CustomClientTest):

    def setUp(self):
        super(CustomClientDeleteTest, self).setUp()

    def test_delete_success(self):
        self.delete_mock.return_value = fakes.FakeResponse()
        self.custom_client.delete(
            self.scenario_name, self.installer_name,
            self.version_name, self.project_name,
            self.custom_raw)
        kall = self.delete_mock.call_args
        args, kwargs = kall
        self.assert_url(
            args[0],
            self.base_url
            + '?installer=installer&version=version&project=project')

    def test_delete_failure(self):
        with testtools.ExpectedException(Exception, 'Delete failed: Error'):
            self.delete_mock.return_value = utils.FAKE_FAILURE
            self.custom_client.delete(
                self.scenario_name, self.installer_name,
                self.version_name, self.project_name,
                self.custom_raw)


class CustomClientUpdateTest(CustomClientTest):

    def setUp(self):
        super(CustomClientUpdateTest, self).setUp()

    def test_update_success(self):
        self.put_mock.return_value = fakes.FakeResponse()
        self.custom_client.update(
            self.scenario_name,
            self.installer_name,
            self.version_name,
            self.project_name,
            self.custom_raw)
        kall = self.put_mock.call_args
        args, kwargs = kall
        self.assert_url(
            args[0],
            self.base_url
            + '?installer=installer&version=version&project=project')

    def test_update_failure(self):
        with testtools.ExpectedException(Exception, 'Update failed: Error'):
            self.put_mock.return_value = utils.FAKE_FAILURE
            self.custom_client.update(
                self.scenario_name,
                self.installer_name,
                self.version_name,
                self.project_name,
                self.custom_raw)
