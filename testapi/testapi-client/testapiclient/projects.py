import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient
from authHandler import AuthHandler
from config import Config


class ProjectBase(Command):
    projects_url = Config.config.get("api", "url") + "/projects"


class ProjectGet(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search projects by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        url = ProjectGet.projects_url
        if parsed_args.name:
            url = url + "?name=" + parsed_args.name
        projects = httpClient.get(url)
        print projects


class ProjectGetOne(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            required=True,
                            help='Search project by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        url = ProjectGet.projects_url + "/" + parsed_args.name
        project = httpClient.get(url)
        print project


class ProjectCreate(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
        parser.add_argument('project',
                            type=json.loads,
                            help='Project create request format :{'
                                 ' "name": (required)"", '
                                 '"description": (optional)""}')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
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


class ProjectDelete(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete project by name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        projects = httpClient.delete(
            ProjectDelete.projects_url + "/" + parsed_args.name,
            User.session)
        print projects


class ProjectPut(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')
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
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed."
                return
        projects = httpClient.put(
            ProjectPut.projects_url + "/" + parsed_args.name,
            User.session,
            parsed_args.project)
        print projects
