#! /usr/bin/env python

import datetime
import json
import os
import subprocess
import traceback
import urlparse
import uuid

import argparse

import conf_utils
import logger_utils
import mongo2elastic_format
import shared_utils

logger = logger_utils.KibanaDashboardLogger('mongo2elastic').get

parser = argparse.ArgumentParser(description='Modify and filter mongo json data for elasticsearch')
parser.add_argument('-od', '--output-destination',
                    default='elasticsearch',
                    choices=('elasticsearch', 'stdout'),
                    help='defaults to elasticsearch')

parser.add_argument('-ml', '--merge-latest', default=0, type=int, metavar='N',
                    help='get entries old at most N days from mongodb and'
                         ' parse those that are not already in elasticsearch.'
                         ' If not present, will get everything from mongodb, which is the default')

parser.add_argument('-e', '--elasticsearch-url', default='http://localhost:9200',
                    help='the url of elasticsearch, defaults to http://localhost:9200')

parser.add_argument('-u', '--elasticsearch-username', default=None,
                    help='The username with password for elasticsearch in format username:password')

args = parser.parse_args()

tmp_docs_file = './mongo-{}.json'.format(uuid.uuid4())


class DocumentPublisher:

    def __init__(self, doc, fmt, exist_docs, creds, to):
        self.doc = doc
        self.fmt = fmt
        self.creds = creds
        self.exist_docs = exist_docs
        self.to = to
        self.is_formatted = True

    def format(self):
        try:
            if self._verify_document() and self.fmt:
                self.is_formatted = vars(mongo2elastic_format)[self.fmt](self.doc)
            else:
                self.is_formatted = False
        except Exception:
            logger.error("Fail in format testcase[%s]\nerror message: %s" %
                         (self.doc, traceback.format_exc()))
            self.is_formatted = False
        finally:
            return self

    def publish(self):
        if self.is_formatted and self.doc not in self.exist_docs:
            self._publish()

    def _publish(self):
        status, data = shared_utils.publish_json(self.doc, self.creds, self.to)
        if status > 300:
            logger.error('Publish record[{}] failed, due to [{}]'
                         .format(self.doc, json.loads(data)['error']['reason']))

    def _fix_date(self, date_string):
        if isinstance(date_string, dict):
            return date_string['$date']
        else:
            return date_string[:-3].replace(' ', 'T') + 'Z'

    def _verify_document(self):
        """
        Mandatory fields:
            installer
            pod_name
            version
            case_name
            date
            project
            details

            these fields must be present and must NOT be None

        Optional fields:
            description

            these fields will be preserved if the are NOT None
        """
        mandatory_fields = ['installer',
                            'pod_name',
                            'version',
                            'case_name',
                            'project_name',
                            'details']
        mandatory_fields_to_modify = {'start_date': self._fix_date}
        fields_to_swap_or_add = {'scenario': 'version'}
        if '_id' in self.doc:
            mongo_id = self.doc['_id']
        else:
            mongo_id = None
        optional_fields = ['description']
        for key, value in self.doc.items():
            if key in mandatory_fields:
                if value is None:
                    # empty mandatory field, invalid input
                    logger.info("Skipping testcase with mongo _id '{}' because the testcase was missing value"
                                " for mandatory field '{}'".format(mongo_id, key))
                    return False
                else:
                    mandatory_fields.remove(key)
            elif key in mandatory_fields_to_modify:
                if value is None:
                    # empty mandatory field, invalid input
                    logger.info("Skipping testcase with mongo _id '{}' because the testcase was missing value"
                                " for mandatory field '{}'".format(mongo_id, key))
                    return False
                else:
                    self.doc[key] = mandatory_fields_to_modify[key](value)
                    del mandatory_fields_to_modify[key]
            elif key in fields_to_swap_or_add:
                if value is None:
                    swapped_key = fields_to_swap_or_add[key]
                    swapped_value = self.doc[swapped_key]
                    logger.info("Swapping field '{}' with value None for '{}' with value '{}'.".format(key, swapped_key,
                                                                                                       swapped_value))
                    self.doc[key] = swapped_value
                    del fields_to_swap_or_add[key]
                else:
                    del fields_to_swap_or_add[key]
            elif key in optional_fields:
                if value is None:
                    # empty optional field, remove
                    del self.doc[key]
                optional_fields.remove(key)
            else:
                # unknown field
                del self.doc[key]

        if len(mandatory_fields) > 0:
            # some mandatory fields are missing
            logger.info("Skipping testcase with mongo _id '{}' because the testcase was missing"
                        " mandatory field(s) '{}'".format(mongo_id, mandatory_fields))
            return False
        elif len(mandatory_fields_to_modify) > 0:
            # some mandatory fields are missing
            logger.info("Skipping testcase with mongo _id '{}' because the testcase was missing"
                        " mandatory field(s) '{}'".format(mongo_id, mandatory_fields_to_modify.keys()))
            return False
        else:
            if len(fields_to_swap_or_add) > 0:
                for key, swap_key in fields_to_swap_or_add.iteritems():
                    self.doc[key] = self.doc[swap_key]

            return True


class DocumentsPublisher:

    def __init__(self, project, case, fmt, days, elastic_url, creds, to):
        self.project = project
        self.case = case
        self.fmt = fmt
        self.days = days
        self.elastic_url = elastic_url
        self.creds = creds
        self.to = to
        self.existed_docs = []

    def export(self):
        if days > 0:
            past_time = datetime.datetime.today() - datetime.timedelta(days=days)
            query = '''{{
                          "project_name": "{}",
                          "case_name": "{}",
                          "start_date": {{"$gt" : "{}"}}
                        }}'''.format(self.project, self.case, past_time)
        else:
            query = '''{{
                           "project_name": "{}",
                           "case_name": "{}"
                        }}'''.format(self.project, self.case)
        cmd = ['mongoexport',
               '--db', 'test_results_collection',
               '--collection', 'results',
               '--query', '{}'.format(query),
               '--out', '{}'.format(tmp_docs_file)]
        try:
            subprocess.check_call(cmd)
            return self
        except Exception, err:
            logger.error("export mongodb failed: %s" % err)
            self._remove()
            exit(-1)

    def get_existed_docs(self):
        self.existed_docs = shared_utils.get_elastic_docs_by_days(self.elastic_url, self.creds, days)
        return self

    def publish(self):
        try:
            with open(tmp_docs_file) as fdocs:
                for doc_line in fdocs:
                    DocumentPublisher(json.loads(doc_line),
                                      self.fmt,
                                      self.existed_docs,
                                      self.creds,
                                      self.to).format().publish()
        finally:
            fdocs.close()
            self._remove()

    def _remove(self):
        if os.path.exists(tmp_docs_file):
            os.remove(tmp_docs_file)


if __name__ == '__main__':
    base_elastic_url = urlparse.urljoin(args.elasticsearch_url, '/test_results/mongo2elastic')
    to = args.output_destination
    days = args.merge_latest
    es_creds = args.elasticsearch_username

    if to == 'elasticsearch':
        to = base_elastic_url

    for project, case_dicts in conf_utils.testcases_yaml.items():
        for case_dict in case_dicts:
            case = case_dict.get('name')
            fmt = conf_utils.compose_format(case_dict.get('format'))
            DocumentsPublisher(project,
                               case,
                               fmt,
                               days,
                               base_elastic_url,
                               es_creds,
                               to).export().get_existed_docs().publish()
