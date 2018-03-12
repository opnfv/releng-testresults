from cliff import command

from testapiclient.utils import url_parse


class Command(command.Command):
    def get_parser(self, prog_name):
        parser = super(Command, self).get_parser(prog_name)
        parser.add_argument('-u',
                            type=str,
                            help='Username for authentication')
        parser.add_argument('-p',
                            type=str,
                            help='Password for authentication')

        return parser

    def show(self, request, response):
        print ' '.join([request,
                        'success' if response.status_code < 300
                        else 'failed: {}'.format(response.reason)])


class Lister(command.Command):

    @staticmethod
    def filter_by(url, parsed_args):
        queries = {}
        for key, value in parsed_args.__dict__.items():
            if value:
                queries[key] = value
        url_filtered = url_parse.query_join(url, **queries)
        return url_filtered

    def show(self, response):
        print response.json() if response.status_code < 300 \
            else 'Get failed: {}'.format(response.reason)


class ShowOne(command.Command):
    def show(self, response):
        print response.json() if response.status_code < 300 \
            else 'Get failed: {}'.format(response.reason)
