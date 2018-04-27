.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.

==============
TestAPI client
==============

TestAPIClient is a command-line client for TestAPI that
brings the command set for pod, project, testcase, results,
deploy result and scenario together in a single shell with a uniform command
structure.


Installation
------------

User can install this client from the source.

.. code-block:: shell

  python install testapi/testapi-client/setup.py install

After the installation, user has to set the environment variables

.. code-block:: shell

   source  testapi/testapi-client/etc/client.creds


Authentication Process
----------------------

User needs to provide the username and the password with the testapi
command.

.. code-block:: shell

    $ testapi -u [username] -p [password]
    (testapi) pod create


or

.. code-block:: shell

    testapi pode create -u [username] -p [password] [pod-schema]

first one, user can continue the progress after the authentication.
cli will create a new session to handle the request.

In second one, cli won't create a session. one time command.

Token is also used for the authorization purpose. User has to obtain the
valid token from the TestAPI comminity and set it in the following file
: **testapi/testapi-client/etc/client.creds**

.. code-block:: shell

   source  testapi/testapi-client/etc/client.creds

=================
Command Structure
=================

TestAPIClient follows a common command Structure.

.. code-block:: shell

    testapi [resource-name] [function] [-u] [username] [-p] [password] [command-arguments]

.. NOTE::
  resource-name : include first order parent name and resource name.

  example:
  scenario installer, scenario version, scenario project, scenario custom,
  scenario trustindicator, scenario score, pod , project, testcase, result,
  deployresult and scenario.

.. NOTE::
  -u and -p are optional commands. The user can decide on them.



*Create*

Authentication required

.. code-block:: shell

    testapi pod create [-u] [username] [-p] [password] [pod-schema]

or

.. code-block:: shell

    $ testapi [-u] [username] [-p] [password]
    (testapi) pod create [pod-schema]

.. NOTE::
  pod-schema - '{"role": "", "name": "", "details": "", "mode": ""}'

*Get*

Authentication is not required

.. code-block:: shell

    testapi pod get [-name] [key-word]

.. NOTE::
   -name is not mandatory. The user can use the -name option to reduce the
   search result otherwise they will get the details about all pods.

*Get one*

Authentication is not required

.. code-block:: shell

    testapi pod getone [name-keyword]

.. NOTE::
   name-keyword is mandatory.


*Get one*

Authentication is required

.. code-block:: shell

    testapi pod delete [-u] [username] [-p] [password] [pod-name]

or

.. code-block:: shell

    $ testapi [-u] [username] [-p] [password]
    (testapi) pod delete [pod-name]

.. NOTE::
   pod-name is mandatory.

*Update*


Authentication required

.. code-block:: shell

    testapi project put [-u] [username] [-p] [password] [project-name] [project-schema]

or

.. code-block:: shell

    $ testapi [-u] [username] [-p] [password]
    (testapi) project put [project-name] [project-schema]

.. NOTE::
  project-schema - '{"name": "", "description": ""}'


There are many arguments for each commands. User can get them using help command in the
cli.

.. code-block:: shell

  pod create --help/-h