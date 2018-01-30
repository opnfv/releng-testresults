import json
from user import User
from cliff.command import Command
from httpClient import HTTPClient
from config import Config

class ResultGet(Command):

    def get_parser(self, prog_name):
        parser = super(ResultGet, self).get_parser(prog_name)
        parser.add_argument('-case', default='')
        parser.add_argument('-build_tag', default='')
        parser.add_argument('-from', default='')
        parser.add_argument('-last', default='')
        parser.add_argument('-scenario', default='')
        parser.add_argument('-trust_indicator', default='')
        parser.add_argument('-period', default='')
        parser.add_argument('-project', default='')
        parser.add_argument('-to', default='')
        parser.add_argument('-version', default='')
        parser.add_argument('-descend', default='')
        parser.add_argument('-criteria', default='')
        parser.add_argument('-installer', default='')
        parser.add_argument('-pod', default='')
        parser.add_argument('-page', default='')
        return parser

    def take_action(self, parsed_args):
        url = Config.config.get(Config.mode, "dev_api_url") + "/results?"
        if parsed_args.case:
            url = url + 'case=' + parsed_args.case + '&'
        if parsed_args.build_tag:
            url = url + 'build_tag=' + parsed_args.build_tag + '&'
        parsed_args_dict = vars(parsed_args)
        if parsed_args_dict['from']:
            url = url + 'from=' + parsed_args_dict['from'] + '&'
        if parsed_args_dict['last']:
            url = url + 'last=' + parsed_args_dict['last'] + '&'
        if parsed_args_dict['scenario']:
            url = url + 'scenario=' + parsed_args_dict['scenario'] + '&'
        if parsed_args_dict['trust_indicator']:
            url = url + 'trust_indicator=' + parsed_args_dict['trust_indicator'] + '&'
        if parsed_args_dict['period']:
            url = url + 'period=' + parsed_args_dict['period'] + '&'
        if parsed_args_dict['project']:
            url = url + 'project=' + parsed_args_dict['project'] + '&'
        if parsed_args_dict['to']:
            url = url + 'to=' + parsed_args_dict['to'] + '&'
        if parsed_args_dict['version']:
            url = url + 'version=' + parsed_args_dict['version'] + '&'
        if parsed_args_dict['descend']:
            url = url + 'descend=' + parsed_args_dict['descend'] + '&'
        if parsed_args_dict['criteria']:
            url = url + 'criteria=' + parsed_args_dict['criteria'] + '&'
        if parsed_args_dict['installer']:
            url = url + 'installer=' + parsed_args_dict['installer'] + '&'
        if parsed_args_dict['pod']:
            url = url + 'pod=' + parsed_args_dict['pod'] + '&'
        if parsed_args_dict['page']:
            url = url + 'page=' + parsed_args_dict['page'] + '&'
        httpClient = HTTPClient.getInstance()
        results = httpClient.get(url)
        print results


class ResultCreate(Command):

    def get_parser(self, prog_name):
        parser = super(ResultCreate, self).get_parser(prog_name)
        parser.add_argument('-token', type=str, required=True, help="Authentication token")
        parser.add_argument('result', type=json.loads, required=True, help='Results Object {"project_name": , "scenario": , "stop_date": , "trust_indicator": {"current":  ,"histories": []},"case_name": , "build_tag": , "public": , "version": , "details": {"failures": , "errors": , "stream": , "testsRun": },"criteria": , "installer": , "pod_name": , "start_date": , "user": }')
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        response = httpClient.post(Config.config.get(Config.mode, "dev_api_url") + "/results", User.session, parsed_args.Result, parsed_args.token)
        if response.status_code == 200:
            print "Result has been successfully created!"
        else:
            print response.text


class ResultPut(Command):

    def get_parser(self, prog_name):
        parser = super(ResultPut, self).get_parser(prog_name)
        parser.add_argument('-token', type=str, required=True, help="Authentication token")
        parser.add_argument('-name', type=str, required=True)
        parser.add_argument('Result', type=json.loads, required=True)
        return parser

    def take_action(self, parsed_args):
        httpClient = HTTPClient.getInstance()
        Results = httpClient.put(Config.config.get(Config.mode, "dev_api_url") + "/Results/" + parsed_args.name, User.session, parsed_args.Result, parsed_args.token)
        print Results
