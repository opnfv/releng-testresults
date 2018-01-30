import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient
from config import Config


class ProjectGet(Command):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name', default='')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        projects = httpClient.get(Config.config.get("api", "dev_api_url") + "/projects?name=" + parsed_args.name)
        print projects


class ProjectCreate(Command):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('project', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        response = httpClient.post(Config.config.get("api", "dev_api_url") + "/projects", User.session, parsed_args.project)
        if response.status_code == 200:
            print "Project has been successfully created!"
        else:
            print response.text


class ProjectDelete(Command):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        projects = httpClient.delete(Config.config.get("api", "dev_api_url") + "/projects/" + parsed_args.name, User.session)
        print projects


class ProjectPut(Command):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True)
        parser.add_argument('project', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        projects = httpClient.put(Config.config.get("api", "dev_api_url") + "/projects/" + parsed_args.name, User.session, parsed_args.project)
        print projects
