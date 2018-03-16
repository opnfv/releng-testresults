import json

from testapiclient.utils import command
from testapiclient.utils import urlparse


def testcases_url(name):
    return urlparse.resource_join('projects', name, 'cases')


def testcase_url(parsed_args):
    return urlparse.path_join(
        testcases_url(parsed_args.project_name), parsed_args.name)


class TestcaseGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(TestcaseGet, self).get_parser(prog_name)
        parser.add_argument('--project-name',
                            required=True,
                            help='Search testcases by project name')
        return parser

    def take_action(self, parsed_args):
        columns = (
            'name',
            '_id',
            'creator',
            'creation_date'
        )
        data = self.app.client_manager.get(
            testcases_url(parsed_args.project_name))
        return self.format_output(columns, data.get('testcases', []))


class TestcaseGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(TestcaseGetOne, self).get_parser(prog_name)
        parser.add_argument('--project-name',
                            required=True,
                            help='Search testcase by project name')
        parser.add_argument('name',
                            help='Search testcase by name')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(testcase_url(parsed_args)))


class TestcaseCreate(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(TestcaseCreate, self).get_parser(prog_name)
        parser.add_argument('--project-name',
                            required=True,
                            help='Create testcase under project name')
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

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.post(
                testcases_url(parsed_args.project_name), parsed_args.testcase))


class TestcaseDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(TestcaseDelete, self).get_parser(prog_name)
        parser.add_argument('--project-name',
                            required=True,
                            type=str,
                            help='Delete testcase by project name')
        parser.add_argument('name',
                            type=str,
                            help='Delete testcase by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(testcase_url(parsed_args))


class TestcasePut(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(TestcasePut, self).get_parser(prog_name)
        parser.add_argument('--project-name',
                            type=str,
                            required=True,
                            help='Update testcase by project name')
        parser.add_argument('name',
                            type=str,
                            help='Update testcase by name')
        parser.add_argument('testcase',
                            type=json.loads,
                            help='Testcase Update request format:\n'
                                 '\'{"run": "", "name": "", "ci_loop": "",'
                                 '"tags": "",\n "url": "", "blocking": "",'
                                 '"domains": "", "dependencies": "",\n '
                                 '"version": "", "criteria": "", "tier": "",'
                                 '"trust": "",\n "catalog_description": "",'
                                 '"description": ""}\'')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.put(
                testcase_url(parsed_args), parsed_args.testcase))
