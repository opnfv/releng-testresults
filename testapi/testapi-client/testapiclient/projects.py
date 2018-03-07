import json

from testapiclient import command
from testapiclient import http_client
from testapiclient import identity
from testapiclient import url_parser

PROJECTS_URL = url_parser.resource_join('projects')


def project_url(parsed_args):
    return url_parser.path_join(PROJECTS_URL, parsed_args.name)


class ProjectGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search projects by name')
        return parser

    def take_action(self, parsed_args):
        url = PROJECTS_URL
        if parsed_args.name:
            url = url_parser.query_join(url,
                                        '?name={}'.format(parsed_args.name))
        projects = http_client.get(url)
        print projects


class ProjectGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ProjectGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            required=True,
                            help='Search project by name')
        return parser

    def take_action(self, parsed_args):
        project = http_client.get(project_url(parsed_args))
        print project


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
        response = http_client.post(PROJECTS_URL,
                                    parsed_args.project)
        if response.status_code == 200:
            print "Project has been successfully created!"
        else:
            print response.text


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
        projects = http_client.delete(project_url(parsed_args))
        print projects


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
        projects = http_client.put(project_url(parsed_args),
                                   parsed_args.project)
        print projects
