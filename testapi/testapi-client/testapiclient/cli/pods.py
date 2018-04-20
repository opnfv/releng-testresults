import json

from testapiclient.client import pods
from testapiclient.utils import command
from testapiclient.utils import urlparse


def pods_url():
    return urlparse.resource_join('pods')


def pod_url(parsed_args):
    return urlparse.path_join(pods_url(), parsed_args.name)


class PodGet(command.Lister):
    "Handle get request for pods"

    def get_parser(self, prog_name):
        parser = super(PodGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search pods using name')
        return parser

    def take_action(self, parsed_args):
        columns = (
            "name",
            "_id",
            "creator",
            "role",
            "mode",
            "creation_date",
        )

        data = self.app.client_manager.get(
            urlparse.query_by(pods_url(), 'name', parsed_args))
        return self.format_output(columns, data.get('pods', []))


class PodGetOne(command.ShowOne):
    "Handle get request for pod by name"

    def get_parser(self, prog_name):
        parser = super(PodGetOne, self).get_parser(prog_name)
        parser.add_argument('name',
                            default='',
                            help='Find pod using name')
        return parser

    def take_action(self, parsed_args):
        return self.format_output(
            self.app.client_manager.get(pod_url(parsed_args)))


class PodCreate(command.ShowOne):
    "Handle post request for pods"

    def get_parser(self, prog_name):
        parser = super(PodCreate, self).get_parser(prog_name)
        parser.add_argument('pod',
                            type=json.loads,
                            help='Pod create request format :\n'
                                 '\'{"role": "", "name": "", "details": "", '
                                 '"mode": ""}\',\n role should be either '
                                 '"community-ci" or "production-ci", and '
                                 'mode should be either "metal" or "virtual.')
        return parser

    def take_action(self, parsed_args):
        client = pods.PodsClient(client_manager=self.app.client_manager)
        return self.format_output(client.create(parsed_args.pod))


class PodDelete(command.Command):
    "Handle delete request for pods"

    def get_parser(self, prog_name):
        parser = super(PodDelete, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Delete pods using name')
        return parser

    def take_action(self, parsed_args):
        return self.app.client_manager.delete(pod_url(parsed_args))
