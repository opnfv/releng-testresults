.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.

=====================
TestAPI client import
=====================

**Python module to communicate with the TestAPI Server**:

This project aims to provide a python module which can communicate with the TestAPI Server.
The user can use this client to fetch/post/modify the resources on the TestAPI Server.

**Usage**

User will get the deserialize Pod objects with the get request

*GET*

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get()

*GET ONE*

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient()
    pod_client.get_one('name')

*CREATE*

There are two ways to create pods, first one using json string,

.. code-block:: shell

    from testapiclient.client import pods

    pod_client = pods.PodsClient(user='test', password='pass')
    pod_client.create({'name': 'test-api', 'mode':'metal',
                    'role':'community_ci', 'details':''}

other one using pod object,

.. code-block:: shell

    from testapiclient.client import pods
    from testapiclient.models import pods as pm

    pod_client = pods.PodsClient(user='test', password='pass')
    pod = pm.Pods(name='test')
