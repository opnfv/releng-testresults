import json

from testapiclient.utils import command
from testapiclient.utils import http_client as client
from testapiclient.utils import identity
from testapiclient.utils import url_parse


def pods_url():
    return url_parse.resource_join('pods')


def pod_url(parsed_args):
    return url_parse.path_join(pods_url(), parsed_args.name)


class PodGet(command.Lister):
    "Handle get request for pods"

    def get_parser(self, prog_name):
        parser = super(PodGet, self).get_parser(prog_name)
        parser.add_argument('-name',
                            default='',
                            help='Search pods using name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(self.filter_by_name(pods_url(), parsed_args)))


class PodGetOne(command.ShowOne):
    "Handle get request for pod by name"

    def get_parser(self, prog_name):
        parser = super(PodGetOne, self).get_parser(prog_name)
        parser.add_argument('name',
                            default='',
                            help='Find pod using name')
        return parser

    def take_action(self, parsed_args):
        self.show(client.get(pod_url(parsed_args)))


class PodCreate(command.Command):
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

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Create',
                  client.post(pods_url(), parsed_args.pod))


class PodDelete(command.Command):
    "Handle delete request for pods"

    def get_parser(self, prog_name):
        parser = super(PodDelete, self).get_parser(prog_name)
        parser.add_argument('name',
                            type=str,
                            help='Delete pods using name')
        return parser

    @identity.authenticate
    def take_action(self, parsed_args):
        self.show('Delete',
                  client.delete(pod_url(parsed_args)))
