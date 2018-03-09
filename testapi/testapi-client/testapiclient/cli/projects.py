import json

from testapiclient.utils import command
from testapiclient.utils import http_client as client
from testapiclient.utils import identity
from testapiclient.utils import url_parse


def projects_url():
    url_parse.resource_join('projects')


def project_url(parsed_args):
    return url_parse.path_join(projects_url(), parsed_args.name)


class ProjectGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search projects by name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(self.filter_name(projects_url(), parsed_args)))


class ProjectGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ProjectGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            required=True,
                            help='Search project by name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(project_url(parsed_args)))


class ProjectCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('project',
                            type=json.loads,
                            help='Project create request format :{'
                                 ' "name": (required)"", '
                                 '"description": (optional)""}')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Create',
                  client.post(projects_url(), parsed_args.project))


class ProjectDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete project by name')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Delete',
                  client.delete(project_url(parsed_args)))


class ProjectPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Update project by name')
        parser.add_argument('project',
                            type=json.loads,
                            help='Project Update request format :{'
                                 '"name": (required)"", '
                                 '"description": (optional)""}')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Update',
                  client.put(project_url(parsed_args), parsed_args.project))
