.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0


*****************************
Web Portal for OPNFV Test API
*****************************

Author: Tharmarajasingam Thuvarakan Mentors: S. Feng, J.Lausuch, M.Richomme

Abstract
========

TestAPI is used by all the test projects to report results. It is also used to declare projects,
test cases and labs. It is defined in Functest developer guide. The internship aims to add web
portal for TestAPI. The showcase user got through the web portal, will be more human-friendly
compared to the swagger page. Also, internship aims to build a python client to reduce the workload.
Python client can be used as a python module.

Overview
========

The internship time period was from Oct 9th to May 18th. The project proposal page is here [1]_. 
The intern project was assigned to Svk Rohit and was mentored by S. Feng, J.Lausuch, M.Richomme. 
The link to the patches submitted is [2]_. The internship was successfully completed and the 
documentation is as follows.

.. [1] https://wiki.opnfv.org/display/DEV/Intern+Project%3A+Web+Portal+for+OPNFV+Test+API

.. [2] https://gerrit.opnfv.org/gerrit/#/q/status:merged+owner:%22Thuvarakan+Tharmarajasingam+%253Ctharma.thuva%2540gmail.com%253E%22


Problem Statement
=================

The following were to be accomplished within the internship time frame.

* Redesign the website theme

    Change the exixtsing theme of the frontend and design a unified theme.

* Add separate pages to each resource

    Creata a separate web page for each resource in the new theme. 

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
