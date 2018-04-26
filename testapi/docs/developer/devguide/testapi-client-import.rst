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

User will get the json Pod objects with the get request.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get()

User can use search parameters to get pods

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get(name='pod1')

GET ONE
"""""""

User will get the json Pod objects with the get request.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get_one('name')

CREATE
""""""
User has to authenticate before running the function.

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient(user='test', password='pass')
    pod_client.create({'name': 'test-api', 'mode':'metal',
                    'role':'community_ci', 'details':''}

