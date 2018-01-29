'use strict';

var mock = require('protractor-http-mock');
var baseURL = "http://localhost:8000/"

describe('testing the result page for anonymous user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/pods',
                    method: 'GET'
                },
                response: {
                    data: {
                        pods: [{role: "community-ci", name: "test", owner: "testUser",
                        details: "DemoDetails", mode: "metal", _id: "59f02f099a07c84bfc5c7aed",
                        creation_date: "2017-10-25 11:58:25.926168"}]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1'
                    }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d62",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1',
                        installer: 'daisy'
                      }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d63",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1',
                        installer: 'daisy',
                        job_name: 'daisy-deploy-baremetal-daily-master'
                      }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d64",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            }
        ]);
    });

    afterEach(function(){
        mock.teardown();
    });

    it( 'should show the deploy results page for anonymous user', function() {
        browser.get(baseURL+"#/deployresults");
        expect(element(by.cssContainingText(".ng-binding.ng-scope","Deploy Results")).isDisplayed()).toBe(true);
    });

    it( 'navigate anonymous user to results page', function() {
        browser.get(baseURL);
        var resultLink = element(by.linkText('Deploy Results')).click();
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/deployresults'), 10000);
    });

    it('Should show the results in results page for anonymous user ', function () {
        browser.get(baseURL+"#/deployresults");
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d62");
    });

    it('Should show the results in results page related to the filters for anonymous user ', function () {
        browser.get(baseURL+"#/deployresults");
        var filter = element(by.model('ctrl.filter'));
        var filterText = element(by.model('ctrl.filterText'));
        filter.sendKeys('installer');
        filterText.sendKeys('daisy');
        var buttonFilter = element(by.buttonText('Filter'));
        buttonFilter.click();
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d63");
        filter.sendKeys('job_name');
        filterText.sendKeys('daisy-deploy-baremetal-daily-master')
        buttonFilter.click();
        expect(cells.get(0).getText()).toContain("3c9f8d64");
    });
    it('Should not show the results in results page related to the filters for anonymous user ', function () {
        browser.get(baseURL+"#/deployresults");
        var filter = element(by.model('ctrl.filter'));
        var filterText = element(by.model('ctrl.filterText'));
        filter.sendKeys('installer');
        filterText.sendKeys('daisyl');
        var buttonFilter = element(by.buttonText('Filter'));
        buttonFilter.click();
        expect(element(by.css('.alert.alert-danger.ng-binding.ng-scope'))
            .isDisplayed()).toBe(true);
    });

});

describe('testing the result page for user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/pods',
                    method: 'GET'
                },
                response: {
                    data: {
                        pods: [{role: "community-ci", name: "test", owner: "testUser",
                        details: "DemoDetails", mode: "metal", _id: "59f02f099a07c84bfc5c7aed",
                        creation_date: "2017-10-25 11:58:25.926168"}]
                    }
                }
            },
            {
                request: {
                path: '/api/v1/profile',
                method: 'GET'
                },
                response: {
                    data: {
                        "fullname": "Test User", "_id": "79f82eey9a00c84bfhc7aed",
                        "user": "testUser", "groups": ["opnfv-testapi-users"],
                        "email": "testuser@test.com"
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1'
                    }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d62",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1',
                        installer: 'daisy'
                      }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d63",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/deployresults',
                    method: 'GET',
                    queryString: {
                        page: '1',
                        installer: 'daisy',
                        job_name : 'daisy-deploy-baremetal-daily-master'
                      }
                },
                response: {
                    data: {
                        "pagination": {
                          "current_page": 1,
                          "total_pages": 1
                        },
                        "deployresults": [
                          {
                            "build_id": 411,
                            "upstream_build_id": 184,
                            "scenario": "os-nosdn-nofeature-ha",
                            "stop_date": "2018-01-2723:21:31.3N",
                            "start_date": "2018-01-2723:21:28.3N",
                            "upstream_job_name": "daisy-os-nosdn-nofeature-ha-baremetal-daily-master",
                            "version": "master",
                            "pod_name": "zte-pod",
                            "criteria": "PASS",
                            "installer": "daisy",
                            "_id": "5a6dc1089a07c80f3c9f8d64",
                            "job_name": "daisy-deploy-baremetal-daily-master",
                            "details": null
                          }
                        ]
                    }
                }
            }
        ]);
    });

    afterEach(function(){
        mock.teardown();
    });

    it( 'should show the deploy results page for user', function() {
        browser.get(baseURL+"#/deployresults");
        expect(element(by.cssContainingText(".ng-binding.ng-scope","Deploy Results")).isDisplayed()).toBe(true);
    });

    it( 'navigate user to results page', function() {
        browser.get(baseURL);
        var resultLink = element(by.linkText('Deploy Results')).click();
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/deployresults'), 10000);
    });

    it('Should show the results in results page for user ', function () {
        browser.get(baseURL+"#/deployresults");
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d62");
    });

    it('Should show the results in results page related to the filters for user ', function () {
        browser.get(baseURL+"#/deployresults");
        var filter = element(by.model('ctrl.filter'));
        var filterText = element(by.model('ctrl.filterText'));
        filter.sendKeys('installer');
        filterText.sendKeys('daisy');
        var buttonFilter = element(by.buttonText('Filter'));
        buttonFilter.click();
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d63");
        filter.sendKeys('job_name');
        filterText.sendKeys('daisy-deploy-baremetal-daily-master')
        buttonFilter.click();
        expect(cells.get(0).getText()).toContain("3c9f8d64");
    });
    it('Should not show the results in results page related to the filters for user ', function () {
        browser.get(baseURL+"#/deployresults");
        var filter = element(by.model('ctrl.filter'));
        var filterText = element(by.model('ctrl.filterText'));
        filter.sendKeys('installer');
        filterText.sendKeys('daisy1');
        var buttonFilter = element(by.buttonText('Filter'));
        buttonFilter.click();
        expect(element(by.css('.alert.alert-danger.ng-binding.ng-scope'))
            .isDisplayed()).toBe(true);
    });

    it('Clear the filter', function () {
        browser.get(baseURL+"#/deployresults");
        var filter = element(by.model('ctrl.filter'));
        var filterText = element(by.model('ctrl.filterText'));
        filter.sendKeys('installer');
        filterText.sendKeys('daisy');
        var buttonFilter = element(by.buttonText('Filter'));
        buttonFilter.click();
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d63");
        var buttonClear = element(by.buttonText('Clear'));
        buttonClear.click();
        var row = element.all(by.repeater('(index, result) in ctrl.data.deployresults')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("3c9f8d62");
    });

    it('view the deploy results ', function () {
		browser.get(baseURL+"#/deployresults");
		var viewOperation = element(by.linkText('3c9f8d62'))
        viewOperation.click();
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains('#/deployresults/5a6dc1089a07c80f3c9f8d62'), 10000);
	});

});