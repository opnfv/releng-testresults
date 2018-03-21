import json

from testapiclient.utils import command
from testapiclient.utils import urlparse


def installers_url(name):
    return urlparse.resource_join('scenarios', name, 'installers')


def installer_url(parsed_args):
    return urlparse.path_join(
        installers_url(parsed_args.scenario_name), parsed_args.name)


class InstallerCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerCreate, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            help='Create installer under scenario name')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'[{"installer": "","versions": []}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.post(
            installers_url(parsed_args.scenario_name), parsed_args.installer)


class InstallerDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerDelete, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            type=str,
                            help='Delete installer by scenario name')
        parser.add_argument('name',
                            nargs='+',
                            help='Delete installer by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(
            installers_url(parsed_args.scenario_name), parsed_args.name)


class InstallerPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerPut, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Update installer by scenario name')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'[{"installer": "","versions": []}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.put(
            installers_url(
                parsed_args.scenario_name), parsed_args.installer)
