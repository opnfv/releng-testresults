import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient
from config import Config


class ProjectBase(Command):
    projects_url = Config.config.get("api", "url") + "/projects"


class ProjectGet(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name', default='', help='Search project by name')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        url = ProjectGet.projects_url
        if parsed_args.name:
            url = ProjectGet.projects_url + "?name=" + parsed_args.name
        projects = http_client.get(url)
        print projects


class ProjectCreate(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('project', type=json.loads, help='Project create request format:\n{ "name": " ", "description": " "},\n name - required ; description - optional')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        response = http_client.post(ProjectCreate.projects_url, User.session, parsed_args.project)
        if response.status_code == 200:
            print "Project has been successfully created!"
        else:
            print response.text


class ProjectDelete(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True, help='Delete project by name')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        projects = http_client.delete(ProjectDelete.projects_url + "/" + parsed_args.name, User.session)
        print projects


class ProjectPut(ProjectBase):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True, help='Update project by name')
        parser.add_argument('project', type=json.loads, help='Project update request format:\n{ "name": " ", "description": " "},\n name - required ; description - optional')
        return parser

    def take_action(self, parsed_args):
        http_client = HTTPClient.get_Instance()
        projects = http_client.put(ProjectPut.projects_url + "/" + parsed_args.name, User.session, parsed_args.project)
        print projects
