import json
import ast

from user import User
from cliff.command import Command
from httpClient import HTTPClient
from authHandler import AuthHandler
from config import Config


class ScenarioBase(Command):
    scenario_url = Config.config.get("api", "url") + "/scenarios"


class ScenarioGet(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioGet, self).get_parser(prog_name)
        parser.add_argument('-name', type=str, help='Search scenarios using name')
        parser.add_argument('-installer', type=str, help='Search scenarios using installer')
        parser.add_argument('-version', type=str, help='Search scenarios using version')
        parser.add_argument('-project', type=str, help='Search scenarios using project')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        req_url = ScenarioGet.scenario_url + "?"
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


class ScenarioCreate(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioCreate, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('scenario', type=json.loads, help='''Scenario create request format :
        \n\'{ "installers": [], "name": "os-Fake-ha"}\',\n
        Intaller create request format :\n
        \'{"installer": "","versions": []}\',\n
        Version create request format :\n
        \'{"owner": "","version": "","projects": []}\',\n
        Project create request format :\n
        \'{"project": "","customs": [],"scores": [],"trust_indicators": []}\',\n
        Custom create request format :\n
        \'["asf","saf"]\',\n
        Score create request format :\n
        \'{"date": "", "score": ""}\',\n
        Trust Indicators create request format :\n
        \'{"date": "", "status": ""}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        response = httpClient.post(ScenarioCreate.scenario_url, User.session, parsed_args.scenario)
        if response.status_code == 200:
            print "Scenario has been successfully created!"
        else:
            print response.text


class ScenarioDelete(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioDelete, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-name', type=str, required=True, help='Delete Scenario using name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        Scenarios = httpClient.delete(ScenarioDelete.scenario_url + "/" + parsed_args.name, User.session)
        print Scenarios


class ScenarioPut(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioPut, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-name', type=str, required=True, help='Update Scenario using name')
        parser.add_argument('scenario', type=json.loads, help='''Scenario Update request format :
        \n\'{ "installers": [], "name": "os-Fake-ha"}\',\n
        Intaller create request format :\n
        \'{"installer": "installer1","versions": []}\',\n
        Version create request format :\n
        \'{"owner": "","version": "","projects": []}\',\n
        Project create request format :\n
        \'{"project": "","customs": [],"scores": [],"trust_indicators": []}\',\n
        Custom create request format :\n
        \'[""]\',\n
        Score create request format :\n
        \'{"date": "", "score": ""}\',\n
        Trust Indicators create request format :\n
        \'{"date": "", "status": ""}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        Scenarios = httpClient.put(ScenarioPut.scenario_url + "/" + parsed_args.name, User.session, parsed_args.scenario)
        print Scenarios


class ScenarioAddScore(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddScore, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add Score by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add Score by installer name')
        parser.add_argument('-version', type=str, required=True, help='Add Score by version name')
        parser.add_argument('-project', type=str, required=True, help='Add Score by project name')
        parser.add_argument('score', type=json.loads, help='''Score create request format :
        \'{"date": "", "score": ""}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddScore.scenario_url + "/" + parsed_args.scenario + "/scores?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, parsed_args.score)
        if response.status_code == 200:
            print "Scenario has been successfully created!"
        else:
            print response.text


class ScenarioAddTI(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddTI, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add Trust Indicator by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add Trust Indicator by installer name')
        parser.add_argument('-version', type=str, required=True, help='Add Trust Indicator by version name')
        parser.add_argument('-project', type=str, required=True, help='Add Trust Indicator by project name')
        parser.add_argument('ti', type=json.loads, help='''Trust Indicator create request format :
        \'{"date": "", "status": ""}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddTI.scenario_url + "/" + parsed_args.scenario + "/trust_indicators?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, parsed_args.ti)
        if response.status_code == 200:
            print "Trust Indicator has been successfully created!"
        else:
            print response.text


class ScenarioAddCustom(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddCustom, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add custom by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add custom by installer name')
        parser.add_argument('-version', type=str, required=True, help='Add custom by version name')
        parser.add_argument('-project', type=str, required=True, help='Add custom by project name')
        parser.add_argument('custom', help='''Custom create request format :
        \'[""]\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddCustom.scenario_url + "/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.post(req_url, User.session, ast.literal_eval(parsed_args.custom))
        if response.status_code == 200:
            print "Custom has been successfully created!"
        else:
            print response.text


class ScenarioUpdateCustom(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioUpdateCustom, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='update custom by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='update custom by installer name')
        parser.add_argument('-version', type=str, required=True, help='update custom by version name')
        parser.add_argument('-project', type=str, required=True, help='update custom by project name')
        parser.add_argument('custom', help='''Custom update request format :
        \'[""]\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioUpdateCustom.scenario_url + "/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.put(req_url, User.session, ast.literal_eval(parsed_args.custom))
        print response


class ScenarioDeleteCustom(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteCustom, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Delete custom by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Delete custom by installer name')
        parser.add_argument('-version', type=str, required=True, help='Delete custom by version name')
        parser.add_argument('-project', type=str, required=True, help='Delete custom by project name')
        parser.add_argument('-custom', required=True, help='Delete custom by custom name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioDeleteCustom.scenario_url + "/" + parsed_args.scenario + "/customs?installer=" + parsed_args.installer + "&version=" + parsed_args.version + "&project=" + parsed_args.project
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.custom))
        print response


class ScenarioAddProject(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddProject, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add project by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add project by installer name')
        parser.add_argument('-version', type=str, required=True, help='Add project by version name')
        parser.add_argument('project', type=json.loads, help='''Project create request format :
        \'{"project": "","customs": [],"scores": [],"trust_indicators": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        projects = []
        projects.append(parsed_args.project)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddProject.scenario_url + "/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer + "&version=" + parsed_args.version
        response = httpClient.post(req_url, User.session, projects)
        if response.status_code == 200:
            print "Projects has been successfully created!"
        else:
            print response.text


class ScenarioUpdateProject(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioUpdateProject, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add project by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add project by installer name')
        parser.add_argument('-version', type=str, required=True, help='Add project by version name')
        parser.add_argument('project', type=json.loads, help='''Project create request format :
        \'{"project": "","customs": [],"scores": [],"trust_indicators": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        projects = []
        projects.append(parsed_args.project)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddProject.scenario_url + "/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer + "&version=" + parsed_args.version
        response = httpClient.put(req_url, User.session, projects)
        if response.status_code == 200:
            print "Projects has been successfully updated!"
        else:
            print response.text


class ScenarioDeleteProject(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteProject, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Delete project by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Delete project by installer name')
        parser.add_argument('-version', type=str, required=True, help='Delete project by version name')
        parser.add_argument('-project', required=True, help='Delete project by project name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioDeleteProject.scenario_url + "/" + parsed_args.scenario + "/projects?installer=" + parsed_args.installer + "&version=" + parsed_args.version
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.project))
        print response


class ScenarioAddVersion(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddVersion, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add version by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Add version by installer name')
        parser.add_argument('version', type=json.loads, help='''version create request format :
        \'{"owner": "","version": "","projects": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        versions = []
        versions.append(parsed_args.version)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddVersion.scenario_url + "/" + parsed_args.scenario + "/versions?installer=" + parsed_args.installer
        response = httpClient.post(req_url, User.session, versions)
        if response.status_code == 200:
            print "Version has been successfully created!"
        else:
            print response.text


class ScenarioPutVersion(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioPutVersion, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Update version by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Update version by installer name')
        parser.add_argument('version', type=json.loads, help='''version update request format :
        \'{"owner": "","version": "","projects": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        versions = []
        versions.append(parsed_args.version)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioPutVersion.scenario_url + "/" + parsed_args.scenario + "/versions?installer=" + parsed_args.installer
        response = httpClient.put(req_url, User.session, versions)
        if response.status_code == 200:
            print "Version has been successfully Updated!"
        else:
            print response.text


class ScenarioDeleteVersion(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteVersion, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Delete version by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Delete version by installer name')
        parser.add_argument('-version', required=True, help='Delete version by version name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioPutVersion.scenario_url + "/" + parsed_args.scenario + "/versions?installer=" + parsed_args.installer
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.version))
        print response


class ScenarioAddInstaller(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioAddInstaller, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add installer by scenario name')
        parser.add_argument('installer', type=json.loads, help='''installer create request format :
        \'{"installer": "installer1","versions": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        installers = []
        installers.append(parsed_args.installer)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioAddInstaller.scenario_url + "/" + parsed_args.scenario + "/installers"
        response = httpClient.post(req_url, User.session, installers)
        if response.status_code == 200:
            print "Installer has been successfully created!"
        else:
            print response.text


class ScenarioPutInstaller(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioPutInstaller, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Add installer by scenario name')
        parser.add_argument('installer', type=json.loads, help='''installer create request format :
        \'{"installer": "installer1","versions": []}\'''')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        installers = []
        installers.append(parsed_args.installer)
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioPutInstaller.scenario_url + "/" + parsed_args.scenario + "/installers"
        response = httpClient.put(req_url, User.session, installers)
        if response.status_code == 200:
            print "Installer has been successfully created!"
        else:
            print response.text


class ScenarioDeleteInstaller(ScenarioBase):

    def get_parser(self, prog_name):
        parser = super(ScenarioDeleteInstaller, self).get_parser(prog_name)
        parser.add_argument('-u', type=str, help='Username for authentication')
        parser.add_argument('-p', type=str, help='Password for authentication')
        parser.add_argument('-scenario', type=str, required=True, help='Delete version by scenario name')
        parser.add_argument('-installer', type=str, required=True, help='Delete version by installer name')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.get_Instance()
        if(parsed_args.u and parsed_args.p):
            response = AuthHandler.authenticate(parsed_args.u, parsed_args.p)
            if "login" in response.text:
                print "Authentication has failed. Please check your username and password."
                return
        req_url = ScenarioDeleteInstaller.scenario_url + "/" + parsed_args.scenario + "/installers"
        response = httpClient.delete(req_url, User.session, ast.literal_eval(parsed_args.installer))
        print response
