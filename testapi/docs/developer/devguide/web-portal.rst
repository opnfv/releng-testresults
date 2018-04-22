.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.

==========
Web portal
==========

**Web-portal of OPNFV Testapi**:

This project aims to provide the web interface for the Testapi framework. It uses the Restful APIs
of the testapi framework to provide front-end functionalities.

If you are interested in how TestAPI looks like, please visit OPNFV's official `TestAPI Server`__

.. __: http://testresults.opnfv.org/test

Pre-requsites
=============

In the web portal, we are using AngularJS(1.3.15) as the frontend framework with Bootstrap(v3) CSS.

Running locally
===============

Installation
^^^^^^^^^^^^

Web portal will be installed with the testapi framework. No extra installation.

.. code-block:: shell

    python setup.py install

Start Server
^^^^^^^^^^^^

.. code-block:: shell

    *opnfv-testapi [--config-file <config.ini>]*

If --config-file is provided, the specified configuration file will be employed
when starting the server, or else /etc/opnfv_testapi/config.ini will be utilized
by default.

After executing the command successfully, a TestAPI server will be started on
port 8000, to visit web portal, please access http://hostname:8000

Test
===============

There are few external requirements for the testing.
They are

1. npm : node package manager
    you can get the installation package for nodejs from the official `website`__

    .. __: https://nodejs.org/en/

2. grunt cli : Automation tool

.. code-block:: shell

    npm install -g grunt-cli

After installing global dependencies, you have to install the required local node modules.

.. code-block:: shell

    npm install

**Running tests**

.. code-block:: shell

    grunt e2e

Authentication
==============

The web portal is using Linux identity server as the Central Authentication Service. The following diagram will explain the
authentication process.

.. image:: /images/CAS-sequence.jpg
 :alt: Workflow of the Athentication

When a new user initially logs into an application they won't have established a
session with the application. Instead of displaying a login form asking for the username and password,
the application (via the CAS Client) will redirect the browser to the linux foundation login page.
Linux foundation identity server then authenticates the user. If the authentication fails, the Linux foundation
login page is displayed again with an error message. So until authentication succeeds, the user will not be returned to the application.

Authorization
=============

TestAPI has 3 level authorization layer. They are

**Public**

The public can view the resources(pod, project, testcase, result, deploy result, scenario). They do not have the access to 
create, delete or modify the resources.

**User - Contributors**

Contributors level user can view all the resources(pod, project, testcase, result, deploy result, scenario). They can
create/delete/modify pod and scenario. They do not have the access to create project or testcase.

**User - Submitter**

Submitter level user can view all the resources(pod, project, testcase, result, deploy result, scenario). They can
create/delete/modify pod, scenario, project, and testcase.

Currently, we can't create/modify/delete results or deploy results from the web portal. 

