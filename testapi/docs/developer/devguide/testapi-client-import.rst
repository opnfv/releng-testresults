.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.

=====================
TestAPI client import
=====================

**Python module to communicate with the TestAPI Server**

This project aims to provide a python module which can
communicate with the TestAPI Server. The user can use this client
to fetch/post/modify the resources on the TestAPI Server.

Usage
-----

Pod
^^^

GET
"""

Get a list of all the declared pods from the TestAPI server.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get()

The user can filter the results by the name attribute. Backend will
use a regular expression to find the list of pods which are
related to given name.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get(name='pod1')

.. NOTE::
  Response format: [{"_id": "", "creator": "", "role": "", "name": "",
  "details": "", "mode": "", "creation_date": ""}]


GET ONE
"""""""

Get a specific pod by its name.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get_one('name')

.. NOTE::
  Response format: {"_id": "", "creator": "", "role": "", "name": "",
  "details": "", "mode": "", "creation_date": ""}

CREATE
""""""
This method used to create a project on the server.
The user has to authenticate before running the function.

Input for the function :

  * pod-json : Json object of the project

.. NOTE::
  pod-json-schema - '{"role": "", "name": "", "details": "", "mode": ""}'

  *  role should be either "community-ci" or "production-ci" 
  *  mode should be either "metal" or "virtual"

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient(user='test', password='pass')
    pod_client.create({'name': 'test-api', 'mode':'metal',
                    'role':'community_ci', 'details':''})


Project
^^^^^^^

GET
"""

Get a list of all the declared projects from the TestAPI server.

.. code-block:: shell

    from testapiclient.client import projects

    project_client = projects.ProjectsClient()
    project_client.get()

User can filter the results by the name attribute. Backend will
use a regular expression to find the list of projects which are
related to given name.

.. code-block:: shell

    from testapiclient.client import projects

    project_client = projects.ProjectsClient()
    project_client.get(name='project1')

.. NOTE::
  Response format: [{"_id": "", "creator": "", "description": "",
  "name": "", "creation_date": ""}]

GET ONE
"""""""

Get a specific project by its name.

.. code-block:: shell

    from testapiclient.client import projects

    project_client = projects.ProjectsClient()
    project_client.get_one('name')

.. NOTE::
  Response format: {"_id": "", "creator": "", "description": "",
  "name": "", "creation_date": ""}

CREATE
""""""

This method used to create a project on the server.
User has to authenticate before running the function.

Input for the function :

  * project-json : Json object of the project

.. NOTE::
  project-json schema - '{"description": "", "name": ""}'

.. code-block:: shell

    from testapiclient.client import projects

    project_client = projects.ProjectsClient(user='test', password='pass')
    project_client.create({'name': 'functest', 'description':'sample text'}

UPDATE
""""""

This method used to update an existing project on the server.
User has to authenticate before running the function.

Input for the function :

  * project-name: name of the project which user want to update.
  * project-json: Json object of the project

.. NOTE::
  project-json schema - '{"description": "", "name": ""}'

.. code-block:: shell

    from testapiclient.client import projects

    project_client = projects.ProjectsClient(user='test', password='pass')
    project_client.update('functest', {'name': 'functest',
    'description':'updated text'})