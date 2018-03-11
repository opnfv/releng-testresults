import json

from testapiclient.utils import command
from testapiclient.utils import http_client as client
from testapiclient.utils import identity
from testapiclient.utils import url_parse


def testcases_url():
    return url_parse.resource_join('projects/{}/cases')


def testcase_url(parsed_args):
    return url_parse.path_join(testcases_url(), parsed_args.name)


class TestcaseGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(TestcaseGet, self).get_parser(prog_name)
        parser.add_argument('-project',
                            required=True,
                            default='',
                            help='Get all testcases for a project name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(
            self.filter_by_parent(
                testcases_url(), parsed_args)))


class TestcaseGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(TestcaseGetOne, self).get_parser(prog_name)
        parser.add_argument('-project',
                            required=True,
                            default='',
                            help='Get all testcases for a project name')
        parser.add_argument('-name',
                            default='',
                            required=True,
                            help='Search testcase by name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(
            self.filter_by_parent(testcase_url(parsed_args), parsed_args)))


class TestcaseCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(TestcaseCreate, self).get_parser(prog_name)
        parser.add_argument('-project',
                            required=True,
                            default='',
                            help='Get all testcases for a project name')
        parser.add_argument('testcase',
                            type=json.loads,
                            help='Testcase create request format:\n'
                                 '\'{"run": "", "name": "", "ci_loop": "",'
                                 '"tags": "",\n "url": "", "blocking": "",'
                                 '"domains": "", "dependencies": "",\n '
                                 '"version": "", "criteria": "", "tier": "",'
                                 '"trust": "",\n "catalog_description": "",'
                                 '"description": ""}\'')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Create',
                  client.post(
                      self.filter_by_parent(
                          testcases_url(),
                          parsed_args), parsed_args.testcase))


class TestcaseDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(TestcaseDelete, self).get_parser(prog_name)
        parser.add_argument('-project',
                            required=True,
                            default='',
                            help='Get all testcases for a project name')
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete Testcase by name')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Delete',
                  client.delete(
                      self.filter_by_parent(
                          testcase_url(parsed_args), parsed_args)))


class TestcasePut(command.Command):

    def get_parser(self, prog_name):
        parser = super(TestcasePut, self).get_parser(prog_name)
        parser.add_argument('-project',
                            required=True,
                            default='',
                            help='Get all testcases for a project name')
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Update Testcase by name')
        parser.add_argument('testcase',
                            type=json.loads,
                            help='Testcase create request format:\n'
                                 '\'{"run": "", "name": "", "ci_loop": "",'
                                 '"tags": "",\n "url": "", "blocking": "",'
                                 '"domains": "", "dependencies": "",\n '
                                 '"version": "", "criteria": "", "tier": "",'
                                 '"trust": "",\n "catalog_description": "",'
                                 '"description": ""}\'')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Update',
                  client.put(
                      self.filter_by_parent(
                          testcase_url(parsed_args),
                          parsed_args), parsed_args.testcase))
