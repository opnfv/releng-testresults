from cliff import command


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


class Lister(command.Command):
    pass


class ShowOne(command.Command):
    pass
