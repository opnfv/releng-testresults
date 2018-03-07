import json
from user import User
from testapiclient import command
from httpClient import HTTPClient
from testapiclient import identity
from config import Config


PROJECTS_URL = Config.config.get("api", "url") + "/projects"


class ProjectGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search projects by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        url = PROJECTS_URL
        if parsed_args.name:
            url = url + "?name=" + parsed_args.name
        projects = httpClient.get(url)
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
        httpClient = HTTPClient.get_Instance()
        url = PROJECTS_URL + "/" + parsed_args.name
        project = httpClient.get(url)
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

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = identity.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        response = httpClient.post(ProjectCreate.projects_url,
                                   User.session,
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

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = identity.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        projects = httpClient.delete(
            PROJECTS_URL + "/" + parsed_args.name,
            User.session)
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

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = identity.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        projects = httpClient.put(
            PROJECTS_URL + "/" + parsed_args.name,
            User.session,
            parsed_args.project)
        print projects
