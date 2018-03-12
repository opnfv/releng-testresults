import json

from testapiclient.utils import command
from testapiclient.utils import http_client as client
from testapiclient.utils import identity
from testapiclient.utils import url_parse


def scenarios_url():
    return url_parse.resource_join('scenarios')


def scenario_url(parsed_args):
    return url_parse.path_join(scenarios_url(), parsed_args.name)


class ScenarioGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ScenarioGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            help='Search projects by name')
        parser.add_argument('-installer',
                            help='Search scenarios using installer')
        parser.add_argument('---version',
                            help='Search scenarios using version')
        parser.add_argument('-project',
                            help='Search scenarios using project')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(self.filter_by(scenarios_url(), parsed_args)))


class ScenarioGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ScenarioGetOne, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            required=True,
                            help='Get scenario by name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(scenario_url(parsed_args)))


class ScenarioCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioCreate, self).get_parser(prog_name)
        parser.add_argument('scenario',
                            type=json.loads,
                            help='Scenario create request format :\n'
                                 '\'{ "installers": [], "name": ""}\',\n'
                                 'Intaller create request format :\n'
                                 '\'{"installer": "","versions": []}\',\n'
                                 'Version create request format :\n'
                                 '\'{"owner": "","version": "",'
                                 '"projects": []}\',\n'
                                 'Project create request format :\n'
                                 '\'{"project": "","customs": [],'
                                 '"scores": [],'
                                 '"trust_indicators": []}\',\n'
                                 'Custom create request format :\n'
                                 '\'["asf","saf"]\',\n'
                                 'Score create request format :\n'
                                 '\'{"date": "", "score": ""}\',\n'
                                 'Trust Indicators create request format :\n'
                                 '\'{"date": "", "status": ""}\'')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Create',
                  client.post(scenarios_url(), parsed_args.scenario))


class ScenarioDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDelete, self).get_parser(prog_name)
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Delete scenario by name')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Delete',
                  client.delete(scenario_url(parsed_args)))


class ScenarioPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioPut, self).get_parser(prog_name)
        parser.add_argument('-name',
                            type=str,
                            required=True,
                            help='Update project by name')
        parser.add_argument('scenario',
                            type=json.loads,
                            help='Scenario create request format :\n'
                                 '\'{ "installers": [], "name": ""}\',\n'
                                 'Intaller create request format :\n'
                                 '\'{"installer": "","versions": []}\',\n'
                                 'Version create request format :\n'
                                 '\'{"owner": "","version": "",'
                                 '"projects": []}\',\n'
                                 'Project create request format :\n'
                                 '\'{"project": "","customs": [],'
                                 '"scores": [],'
                                 '"trust_indicators": []}\',\n'
                                 'Custom create request format :\n'
                                 '\'["asf","saf"]\',\n'
                                 'Score create request format :\n'
                                 '\'{"date": "", "score": ""}\',\n'
                                 'Trust Indicators create request format :\n'
                                 '\'{"date": "", "status": ""}\'')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Update',
                  client.put(scenario_url(parsed_args), parsed_args.scenario))
