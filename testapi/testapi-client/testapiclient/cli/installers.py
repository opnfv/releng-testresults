import json

from testapiclient.utils import command
from testapiclient.utils import http_client as client
from testapiclient.utils import identity
from testapiclient.utils import url_parse


def installers_url():
    return url_parse.resource_join('scenarios/{}/installers')


class InstallerCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerCreate, self).get_parser(prog_name)
        parser.add_argument('scenario',
                            type=str,
                            help='Create installer under scenario')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'[{"installer": "","versions": []}]\',\n')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        print parsed_args.installer
        self.show('Create',
                  client.post(
                      self.filter_by_parent(
                          installers_url(),
                          parsed_args), parsed_args.installer))


class InstallerDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerDelete, self).get_parser(prog_name)
        parser.add_argument('scenario',
                            type=str,
                            help='Create installer under scenario')
        parser.add_argument('installers',
                            nargs='+',
                            help='delete one or more installers'
                                 'sperated by space:'
                                 'installer1 installer2')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        print parsed_args.installers
        self.show('Delete',
                  client.delete(
                      self.filter_by_parent(
                          installers_url(),
                          parsed_args), parsed_args.installers))


class InstallerPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerPut, self).get_parser(prog_name)
        parser.add_argument('scenario',
                            type=str,
                            help='Create installer under scenario')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Installer Update request format :{'
                                 '"name": (required)"", '
                                 '"description": (optional)""}')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Update',
                  client.put(
                      self.filter_by_parent(
                          installers_url(),
                          parsed_args), parsed_args.installer))
