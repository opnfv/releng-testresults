import json

from testapiclient.utils import command
from testapiclient.utils import urlparse
from testapiclient.models import project


def projects_url():
    return urlparse.resource_join('projects')


def project_url(parsed_args):
    return urlparse.path_join(projects_url(), parsed_args.name)


class ProjectGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ProjectGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            help='Search projects by name')
        return parser

    def take_action(self, parsed_args):
        columns = (
            'name',
            '_id',
            'creator',
            'creation_date'
        )
        data = self.app.client_manager.get(
            urlparse.query_by(projects_url(), 'name', parsed_args))
        return self.format_output(columns, data.get('projects', []))


class ProjectGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ProjectGetOne, self).get_parser(prog_name)
        parser.add_argument('name',
                            help='Search project by name')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(project_url(parsed_args)))


class ProjectCreate(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ProjectCreate, self).get_parser(prog_name)
        parser.add_argument('project',
                            type=json.loads,
                            help='Project create request format :"' +
                                 str(
                                     project.ProjectCreateRequest().__dict__
                                     ) +
                                 '"')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.post(projects_url(), parsed_args.project))


class ProjectDelete(command.Command):

    def get_parser(self, prog_name):
        parser = super(ProjectDelete, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Delete project by name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(project_url(parsed_args))


class ProjectPut(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ProjectPut, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Update project by name')
        parser.add_argument('project',
                            type=json.loads,
                            help='Project Update request format :"' +
                                 str(
                                     project.ProjectCreateRequest().__dict__
                                     ) + '"'
                            )
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.put(
                project_url(parsed_args), parsed_args.project))
