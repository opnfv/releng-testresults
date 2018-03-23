import json

from testapiclient.utils import command
from testapiclient.utils import urlparse


def scenarios_url():
    return urlparse.resource_join('scenarios')


def scenario_url(parsed_args):
    return urlparse.path_join(scenarios_url(), parsed_args.name)


def resources_url(name, resuorce):
    return urlparse.resource_join('scenarios', name, resuorce)


class ScenarioGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ScenarioGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            help='Search scenarios using name')
        parser.add_argument('-installer',
                            help='Search scenarios using installer')
        parser.add_argument('---version',
                            help='Search scenarios using version')
        parser.add_argument('-project',
                            help='Search scenarios using project')
        return parser

    def take_action(self, parsed_args):
        columns = (
            'name',
            '_id',
            'creator',
            'creation_date'
        )
        data = self.app.client_manager.get(
            urlparse.query_by(scenarios_url(),
                              ['name', 'installer', 'version', 'project'],
                              parsed_args))
        return self.format_output(columns, data.get('scenarios', []))


class ScenarioGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ScenarioGetOne, self).get_parser(prog_name)
        parser.add_argument('name',
                            help='Search scenario by name')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(scenario_url(parsed_args)))


class ScenarioCreate(command.ShowOne):

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

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.post(
                scenarios_url(), parsed_args.scenario))


class ScenarioDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(ScenarioDelete, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Delete scenario by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(scenario_url(parsed_args))


class ScenarioPut(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ScenarioPut, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Update scenario by name')
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

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.put(
                scenario_url(parsed_args), parsed_args.scenario))


class InstallerCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerCreate, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            help='Create installer under scenario name')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'[{"installer": "","versions": []}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.post(
            resources_url(
                parsed_args.scenario_name,
                'installers'), parsed_args.installer)


class InstallerDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerDelete, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            type=str,
                            help='Delete installer by scenario name')
        parser.add_argument('name',
                            nargs='+',
                            help='Delete installer by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(
            resources_url(
                parsed_args.scenario_name,
                'installers'), parsed_args.name)


class InstallerPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(InstallerPut, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Update installer by scenario name')
        parser.add_argument('installer',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'[{"installer": "","versions": []}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.put(
            resources_url(
                parsed_args.scenario_name,
                'installers'), parsed_args.installer)


class VersionCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(VersionCreate, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            help='Create version under scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Create version under scenario name')
        parser.add_argument('version',
                            type=json.loads,
                            help='version create request format :\n'
                                 '\'[{"owner":(string),'
                                 '"version": (string),'
                                 '"projects": (array[ScenarioProject])'
                                 '}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.post(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'versions'),
                'installer',
                parsed_args), parsed_args.version)


class VersionDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(VersionDelete, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            type=str,
                            help='Delete version by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Create version under scenario name')
        parser.add_argument('name',
                            nargs='+',
                            help='Delete version by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'versions'),
                'installer',
                parsed_args), parsed_args.name)


class VersionPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(VersionPut, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Update installer by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Update version under installer name')
        parser.add_argument('version',
                            type=json.loads,
                            help='version update request format :\n'
                                 '\'[{"owner":(string),'
                                 '"version": (string),'
                                 '"projects": (array[ScenarioProject])'
                                 '}]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.put(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'versions'),
                'installer',
                parsed_args), parsed_args.version)


class VersionOwnerPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(VersionOwnerPut, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Update version by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Update version under scenario name')
        parser.add_argument('--version',
                            required=True,
                            help='Update version under scenario name')
        parser.add_argument('owner',
                            type=json.loads,
                            help='Intaller create request format :\n'
                                 '\'{"owner": ""}\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.put(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'owner'),
                ['installer', 'version'],
                parsed_args), parsed_args.owner)


class ProjectCreate(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Create project by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Create project under installer name')
        parser.add_argument('--version',
                            required=True,
                            help='Create project under version name')
        parser.add_argument('project',
                            type=json.loads,
                            help='Project create request format :\n'
                                 '\'[{ "project" (string),'
                                 '"scores": (array[ScenarioScore]),'
                                 '"trust_indicators": (array[ScenarioTI]),'
                                 '"customs": (array[string]) }]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.post(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'projects'),
                ['installer', 'version'],
                parsed_args), parsed_args.project)


class ProjectDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            required=True,
                            type=str,
                            help='Delete projects by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Delete projects under installer name')
        parser.add_argument('--version',
                            required=True,
                            help='Delete projects under version name')
        parser.add_argument('name',
                            nargs='+',
                            help='Delete projects by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'projects'),
                ['installer', 'version'],
                parsed_args), parsed_args.name)


class ProjectPut(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('--scenario-name',
                            type=str,
                            required=True,
                            help='Update project by scenario name')
        parser.add_argument('--installer',
                            required=True,
                            help='Update project under installer name')
        parser.add_argument('--version',
                            required=True,
                            help='Update project under version name')
        parser.add_argument('project',
                            type=json.loads,
                            help='Project update request format :\n'
                                 '\'[{ "project" (string),'
                                 '"scores": (array[ScenarioScore]),'
                                 '"trust_indicators": (array[ScenarioTI]),'
                                 '"customs": (array[string]) }]\',\n')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.put(
            urlparse.query_by(
                resources_url(parsed_args.scenario_name, 'projects'),
                ['installer', 'version'],
                parsed_args), parsed_args.project)
