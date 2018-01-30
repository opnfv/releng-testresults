from setuptools import setup, find_packages

PROJECT = 'testapi-client'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Command line client for testapi',
    long_description=long_description,
    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'testapi = testapi.main:main'
        ],
        'testAPI': [
            'auth = testapi.auth:Auth',

            'pod create = testapi.pods:PodCreate',
            'pod get = testapi.pods:PodGet',
            'pod delete = testapi.pods:PodDelete',
            'pod getone = testapi.pods:PodGetOne',

            'project create = testapi.projects:ProjectCreate',
            'project get = testapi.projects:ProjectGet',
            'project delete = testapi.projects:ProjectDelete',
            'project put = testapi.projects:ProjectPut',

            'testcase create = testapi.testcase:TestCaseCreate',
            'testcase get = testapi.testcase:TestCaseGet',
            'testcase delete = testapi.testcase:TestCaseDelete',
            'testcase put = testapi.testcase:TestCasePut',

            'scenario create = testapi.scenario:ScenarioCreate',
            'scenario get = testapi.scenario:ScenarioGet',
            'scenario delete = testapi.scenario:ScenarioDelete',
            'scenario put = testapi.scenario:ScenarioPut',

            'scenario addscore = testapi.scenario:ScenarioAddScore',

            'scenario addyi = testapi.scenario:ScenarioAddTI',

            'scenario addcustom = testapi.scenario:ScenarioAddCustom',
            'scenario updatecustom = testapi.scenario:ScenarioUpdateCustom',
            'scenario deletecustom = testapi.scenario:ScenarioDeleteCustom',

            'scenario addproject = testapi.scenario:ScenarioAddProject',
            'scenario deleteproject = testapi.scenario:ScenarioDeleteProject',

            'scenario addversion = testapi.scenario:ScenarioAddVersion',
            'scenario deleteversion = testapi.scenario:ScenarioDeleteVersion',
        ]
    },

    zip_safe=False,
)
