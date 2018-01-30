import json
import ast

from user import User
from cliff.command import Command
from httpClient import HTTPClient


class ScenarioGet(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioGet, self).get_parser(prog_name)
        parser.add_argument('-name', type=str)
        parser.add_argument('-installer', type=str)
        parser.add_argument('-version', type=str)
        parser.add_argument('-project', type=str)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios?"
        if(parsed_args.name):
            req_url += "name=" + parsed_args.name + "&"
        if(parsed_args.installer):
            req_url += "installer=" + parsed_args.installer + "&"
        if(parsed_args.version):
            req_url += "version=" + parsed_args.version + "&"
        if(parsed_args.project):
            req_url += "project=" + parsed_args.project
        Scenarios = httpClient.get(req_url)
        print Scenarios


class ScenarioCreate(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioCreate, self).get_parser(prog_name)
        parser.add_argument('scenario', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        response = httpClient.post("http://localhost:8000/api/v1/scenarios", User.session, parsed_args.scenario)
        if response.status_code == 200:
            print "Scenario has been successfully created!"
        else:
            print response.text


class ScenarioDelete(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDelete, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        Scenarios = httpClient.delete("http://localhost:8000/api/v1/scenarios/" + parsed_args.name, User.session)
        print Scenarios


class ScenarioPut(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioPut, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, required=True)
        parser.add_argument('scenario', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        Scenarios = httpClient.put("http://localhost:8000/api/v1/scenarios/" + parsed_args.name, User.session, parsed_args.scenario)
        print Scenarios


class ScenarioAddScore(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddScore, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('score', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/scores?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, parsed_args.score)
        if response.status_code == 200:
            print "Scenario has been successfully created!"
        else:
            print response.text


class ScenarioAddTI(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddTI, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('ti', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/trust_indicators?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, parsed_args.ti)
        if response.status_code == 200:
            print "Trust Indicator has been successfully created!"
        else:
            print response.text


class ScenarioAddCustom(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddCustom, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('custom', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, ast.literal_eval(parsed_args.custom))
        if response.status_code == 200:
            print "Custom has been successfully created!"
        else:
            print response.text


class ScenarioUpdateCustom(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioUpdateCustom, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('custom', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.put(req_url, User.session, ast.literal_eval(parsed_args.custom))
        print response


class ScenarioDeleteCustom(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteCustom, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', type=str, required=True)
        parser.add_argument('-custom', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.custom))
        print response


class ScenarioAddProject(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddProject, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('project', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        projects = []
        projects.append(parsed_args.project)
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer + "&version=" + parsed_args.version
        response = httpClient.post(req_url, User.session, projects)
        if response.status_code == 200:
            print "Projects has been successfully created!"
        else:
            print response.text


class ScenarioDeleteProject(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteProject, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', type=str, required=True)
        parser.add_argument('-project', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer + "&version=" + parsed_args.version
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.project))
        print response


class ScenarioAddVersion(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddVersion, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('version', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        versions = []
        versions.append(parsed_args.version)
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/versions?installer=" + parsed_args.installer
        response = httpClient.post(req_url, User.session, versions)
        if response.status_code == 200:
            print "Version has been successfully created!"
        else:
            print response.text


class ScenarioDeleteVersion(Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteProject, self).get_parser(prog_name)
        parser.add_argument('-scenario', type=str, required=True)
        parser.add_argument('-installer', type=str, required=True)
        parser.add_argument('-version', required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        req_url = "http://localhost:8000/api/v1/scenarios/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.version))
        print response
