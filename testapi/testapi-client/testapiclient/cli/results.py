import json

from testapiclient.utils import command
from testapiclient.utils import urlparse


def results_url():
    return urlparse.resource_join('results')


def result_url(parsed_args):
    return urlparse.path_join(results_url(), parsed_args.result_id)


class ResultGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(ResultGet, self).get_parser(prog_name)
        parser.add_argument('-case',
                            help='Search results using tesetcase')
        parser.add_argument('-build-tag',
                            help='Search results using build tag')
        parser.add_argument('-from',
                            help='Search results using from date')
        parser.add_argument('-last',
                            help='Search results using last date')
        parser.add_argument('-scenario',
                            help='Search results using scenario')
        parser.add_argument('-period',
                            help='Search results using period')
        parser.add_argument('-project',
                            help='Search results using project')
        parser.add_argument('-to',
                            help='Search results using to')
        parser.add_argument('---version',
                            help='Search results using version')
        parser.add_argument('-criteria',
                            help='Search results using version')
        parser.add_argument('-installer',
                            help='Search results using installer')
        parser.add_argument('-pod',
                            help='Search results using pod')
        parser.add_argument('-page',
                            help='Search results using page')
        return parser

    def take_action(self, parsed_args):
        columns = (
            '_id',
            'pod_name',
            'project_name',
            'case_name',
            'version',
            'criteria',
            'start_date',
            'scenario',
            'installer',

        )
        data = self.app.client_manager.get(
            urlparse.query_by(results_url(),
                              ['case', 'build_tag', 'from', 'last',
                               'scenario', 'period', 'project',
                               'to', 'version',
                               'criteria', 'installer', 'pod', 'page'],
                              parsed_args))
        return self.format_output(columns, data.get('results', []))


class ResultGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ResultGetOne, self).get_parser(prog_name)
        parser.add_argument('result_id',
                            help='Search result by result id')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(result_url(parsed_args)))


class ResultCreate(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(ResultCreate, self).get_parser(prog_name)
        parser.add_argument('result',
                            type=json.loads,
                            help='Result create request format:\n'
                                 '\'{"project_name" : "","scenario" : "",'
                                 '"stop_date" : "", "case_name" : "",'
                                 '"build_tag" : "", "version" : "",'
                                 '"pod_name" : "" , "criteria" : "",'
                                 '"installer" : "", "start_date" : "",'
                                 '"details" : ""}\'')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.post(
                results_url(), parsed_args.result))
