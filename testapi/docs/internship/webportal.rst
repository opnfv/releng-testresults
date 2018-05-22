.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


*****************************
Web Portal for OPNFV Test API
*****************************

Author: Tharmarajasingam Thuvarakan Mentors: S. Feng, J.Lausuch, M.Richomme

Abstract
========

TestAPI is used by all the test projects to report results. It is also used to declare projects,
test cases and labs. It is defined in the Functest developer guide. The internship aims to add web
portal for TestAPI. The showcase user got through the web portal, will be more human-friendly
compared to the swagger page. Also, internship aims to build a python client to reduce the workload.
Python client can be used as a python module.

Overview
========

The internship time period was from Oct 9th to May 18th. The project proposal page is here [1]_.
The intern project was assigned to Thuvarakan and was mentored by S. Feng, J.Lausuch, M.Richomme.
The link to the patches submitted is [2]_. The internship was successfully completed and the
documentation is as follows.



Problem Statement
=================

The following were to be accomplished within the internship time frame.

* Redesign the website theme

    Change the existing theme of the frontend and design a unified theme.

* Add separate pages to each resource

    Create a separate web page for each resource in the new theme.

* Implement all the functionalities in the frontend

    Implement the backend functionalities in the frontend for each
    resource.

* Authentication for testapiclient

    Implement the authentication functionality in the testapiclient.

* Add all functionalities to testapiclient

    Implement the backend functionalities in the testapiclient for each
    resource.

* Add support to testapiclient as a python module

    Convert the testapiclient from CLI only to CLI and python module
    mode.


Curation Phase
==============

The curation phase was the first 4 to 8 weeks of the internship. This phase
was to get familiar with the testapi code and functionality and propose the
solutions/tools for the tasks mentioned above.

These are the tools, we proposed for the solutions.

* protractor: An end-to-end test framework for Angular and AngularJS applications

* grunt: A Javascript  task runner, a tool used to automatically perform
          frequent tasks such as minification, compilation, unit testing, and
          linting.

* cliff: Command Line Interface Formulation Framework.


Schedule
========

===================   ========================================================
 Date                 Comment
===================   ========================================================
10th Oct ~17th Oct    Setting up the development environment, design decisions
17th Oct ~ 24th Oct   Pod web portal CRUD
24th Oct ~ 31st Oct   Projects web portal CRUD
13st Oct ~ 7th Nov    Test cases web portal CRUD
7th Nov ~ 14th Nov    Results web portal  R
14th Nov ~ 21st Nov   Results web portal  R
21st Nov ~ 28th Nov   Scenario web portal CRUD
28th Nov ~ 5th Dec    Testapi-client framework
5th Dec ~ 12nd Dec    Pods testapi-client CRUD
12nd Dec ~ 19th Dec   Projects testapi-client CRUD
19th Dec ~ 26th Dec   Test cases testapi-client CRUD
26th Dec ~ 9th Jan    Results testapi-client CRUD
9th Jan ~ 23rd Jan    Scenario testapi-client CRUD
23rd Jan ~ 6th Mar    Bugfix in the frontend and testapiclient
6th Mar ~ 20th Mar    Convert testapiclient to python module
20th Mar ~ 3rd Apr    Testing the python module
3rd Apr ~  9th May    Documentation & Bugfix
===================   ========================================================


FAQ
===


Frontend
********

1. How to add a new test file for the frontend?

  * Frontend test is handled by protractor [3]_ and
    automated by the grunt [4]_. All the tests are located in
    "opnfv_testapi/tests/UI/e2e".
    First, create a text file in the e2e folder. Then add it to the spec
    list in the "opnfv_testapi/ui/Gruntfile.js".


2. How to test application's functionalities interactively?

  * Application requires authentication for many functionalities.
    It will cause time for the developer to check the functionalities.
    Developers can use the application in the authentication false mode.
    To do that, first, change the authenticate to false in the
    "etc/config.ini" file then change the authenticate to false in
    the "opnfv_testapi/ui/config.json" file.


3. Browser does not reflect the code changes, what is it mean?

  * Browser is saving the caches for fast reloadings. Sometime browser
    won't reload the new changes, to solve that we have to clear the browser
    caches.


Testapiclient
*************

1. How to add a new test file for testapiclient?

  * Frontend test is handled by testtools [5]_ and automated by tox [6]_.
    All the tests are located in "testapi-client/tests/unit". Create a text
    file in the unit folder. The name of the test file should start with
    'test\_'. It will automatically add that test file to queue.


2. Difference between client and cli?

  * Client is used to importing testapiclient as a python module.
    The cli folder contained the command line interface for the testapiclient.

References
==========

.. [1] https://wiki.opnfv.org/display/DEV/Intern+Project%3A+Web+Portal+for+OPNFV+Test+API

.. [2] https://gerrit.opnfv.org/gerrit/#/q/status:merged+owner:%22Thuvarakan+Tharmarajasingam+%253Ctharma.thuva%2540gmail.com%253E%22

.. [3] https://www.protractortest.org/

.. [4] https://gruntjs.com

.. [5] https://github.com/testing-cabal/testtools

.. [6] https://tox.readthedocs.io/en/latest/#