import abc
import logging

from cliff import command
from cliff import lister
from cliff import show
import six

from testapiclient.utils import url_parse
from testapiclient import utils


class CommandMeta(abc.ABCMeta):

    def __new__(mcs, name, bases, cls_dict):
        if 'log' not in cls_dict:
            cls_dict['log'] = logging.getLogger(
                cls_dict['__module__'] + '.' + name)
        return super(CommandMeta, mcs).__new__(mcs, name, bases, cls_dict)


@six.add_metaclass(CommandMeta)
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

    def run(self, parsed_args):
        self.log.debug('run(%s)', parsed_args)
        return super(Command, self).run(parsed_args)

    def validate_os_beta_command_enabled(self):
        if not self.app.options.os_beta_command:
            msg = ('Caution: This is a beta command and subject to '
                    'change. Use global option --os-beta-command '
                    'to enable this command.')
            raise Exception(msg)


class Lister(Command, lister.Lister):
    @staticmethod
    def filter_by_name(url, parsed_args):
        def query_url():
            return url_parse.query_join(url, name=parsed_args.name)

        return query_url() if parsed_args.name else url

    @staticmethod
    def format_list(columns, data):
        return (columns,
                (utils.get_item_properties(s, columns) for s in data))



class ShowOne(Command, show.ShowOne):
    @staticmethod
    def format_show(body):
        return zip(*sorted(six.iteritems(body)))
