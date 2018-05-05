import json

from testapiclient.utils import command
from testapiclient.utils import urlparse
from testapiclient.models import deployresult


def deployresults_url():
    return urlparse.resource_join('deployresults')


def deployresult_url(parsed_args):
    return urlparse.path_join(deployresults_url(), parsed_args.deployresult_id)


class DeployresultGet(command.Lister):

    def get_parser(self, prog_name):
        parser = super(DeployresultGet, self).get_parser(prog_name)
        parser.add_argument('-build-id',
                            help='Search deployresults using build tag')
        parser.add_argument('-from',
                            help='Search deployresults using from date')
        parser.add_argument('-scenario',
                            help='Search deployresults using scenario')
        parser.add_argument('-period',
                            help='Search deployresults using period')
        parser.add_argument('-page',
                            help='Search deployresults using page')
        parser.add_argument('-to',
                            help='Search deployresults using to')
        parser.add_argument('---version',
                            help='Search deployresults using version')
        parser.add_argument('-last',
                            help='Search deployresults using last date')
        parser.add_argument('-pod-name',
                            help='Search deployresults using pod')
        parser.add_argument('-criteria',
                            help='Search deployresults using version')
        parser.add_argument('-installer',
                            help='Search deployresults using installer')
        parser.add_argument('-job-name',
                            help='Search deployresults using project')

        return parser

    def take_action(self, parsed_args):
        columns = (
            '_id',
            'pod_name',
            'version',
            'criteria',
            'start_date',
            'stop_date',
            'scenario',
            'installer',

        )
        data = self.app.client_manager.get(
            urlparse.query_by(deployresults_url(),
                              ['build_id', 'from', 'last',
                               'scenario', 'period', 'job_name',
                               'to', 'version',
                               'criteria', 'installer', 'pod_name', 'page'],
                              parsed_args))
        return self.format_output(columns, data.get('deployresults', []))


class DeployresultGetOne(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(DeployresultGetOne, self).get_parser(prog_name)
        parser.add_argument('deployresult_id',
                            help='Search deployresult by deployresult id')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(deployresult_url(parsed_args)))


class DeployresultCreate(command.ShowOne):

    def get_parser(self, prog_name):
        parser = super(DeployresultCreate, self).get_parser(prog_name)
        parser.add_argument('deployresult',
                            type=json.loads,
                            help='Deployresult create request format:\n "' +
                                 str(
                                     deployresult.DeployResultCreateRequest(
                                     ).__dict__) + '"')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.post(
                deployresults_url(), parsed_args.deployresult))
