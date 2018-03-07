import json

from testapiclient import command
from testapiclient import config
from testapiclient import http_client
from testapiclient import identity
from testapiclient import user

PROJECTS_URL = config.Config.config.get("api", "url") + "/projects"


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
            url = url + "?name=" + parsed_args.name
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
        url = PROJECTS_URL + "/" + parsed_args.name
        project = http_client.get(url)
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
        response = http_client.post(ProjectCreate.projects_url,
                                    user.User.session,
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
        projects = http_client.delete(
            PROJECTS_URL + "/" + parsed_args.name,
            user.User.session)
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
        projects = http_client.put(
            PROJECTS_URL + "/" + parsed_args.name,
            user.User.session,
            parsed_args.project)
        print projects
