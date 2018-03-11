from cliff import command

from testapiclient.utils import url_parse


class CommandBase(command.Command):
    @staticmethod
    def filter_by_parent(url, parsed_args):
        if parsed_args.project:
            return url.format(parsed_args.project)
        else:
            return url.format(parsed_args.scenario)


class Command(CommandBase):
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


class Lister(CommandBase):

    @staticmethod
    def filter_by_name(url, parsed_args):
        def query_url():
            return url_parse.query_join(url, name=parsed_args.name)

        return query_url() if parsed_args.name else url

    def show(self, response):
        print response.json() if response.status_code < 300 \
            else 'Get failed: {}'.format(response.reason)


class ShowOne(CommandBase):
    def show(self, response):
        print response.json() if response.status_code < 300 \
            else 'Get failed: {}'.format(response.reason)
