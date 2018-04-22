.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) 2017 ZTE Corp.

==========
Web portal
==========

**Web-portal of OPNFV Test Projects**:

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

    *python setup.py install*

Start Server
^^^^^^^^^^^^

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
    npm install -g grunt-cli

After installing global dependencies, you have to install the required local node modules.
    npm install

**Running tests**

    grunt e2e
