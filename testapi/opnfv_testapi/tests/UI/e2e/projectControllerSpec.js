'use strict';

var mock = require('protractor-http-mock');
var baseURL = "http://localhost:8000/#/"

describe('testing the Project Link for anonymous user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'GET'
                },
                response: {
                    data: {
                        "owner": "thuva4",
                        "_id": "5a0c022f9a07c846d3c2cc94",
                        "creation_date": "2017-11-15 14:30:31.200259",
                        "description": "dsfsd",
                        "name": "testproject"
                    }
                }
            }
        ]);
    });

    afterEach(function(){
		mock.teardown();
	});

    it( 'navigate to the project page', function() {
		browser.get(baseURL+"projects/testproject");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ 'projects/testproject'), 10000);
    });

    it('show the project details for anonymous user ', function(){
        var table = $$('.projects-table.ng-scope tr');
        var projectDetailsLable = ['Name','Description','Creation date']
        var projectDetails = ['testproject', 'dsfsd','2017-11-15 14:30:31.200259']
        table.each(function(row,index) {
            var rowElems = row.$$('td');
            expect(rowElems.count()).toBe(2);
            expect(rowElems.get(0).getText()).toMatch(projectDetailsLable[index]);
            expect(rowElems.get(1).getText()).toMatch(projectDetails[index]);
          });
    });

    it('should not show the update & delete button', function(){
        var buttonUpdate = element(by.buttonText('Update Project'));
        var buttonDelete = element(by.buttonText('Delete Project'));
        expect(buttonUpdate.isDisplayed()).toBeFalsy();
        expect(buttonDelete.isDisplayed()).toBeFalsy();
    });

});


describe('testing the Project Link for user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'GET'
                },
                response: {
                    data: {
                        "owner": "thuva4",
                        "_id": "5a0c022f9a07c846d3c2cc94",
                        "creation_date": "2017-11-15 14:30:31.200259",
                        "description": "dsfsd",
                        "name": "testproject"
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
            }
        ]);
    });

    afterEach(function(){
		mock.teardown();
	});

    it( 'navigate to the project page', function() {
		browser.get(baseURL+"projects/testproject");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ 'projects/testproject'), 10000);
    });

    it('show the project details for anonymous user ', function(){
        var table = $$('.projects-table.ng-scope tr');
        var projectDetailsLable = ['Name','Description','Creation date']
        var projectDetails = ['testproject', 'dsfsd','2017-11-15 14:30:31.200259']
        table.each(function(row,index) {
            var rowElems = row.$$('td');
            expect(rowElems.count()).toBe(2);
            expect(rowElems.get(0).getText()).toMatch(projectDetailsLable[index]);
            expect(rowElems.get(1).getText()).toMatch(projectDetails[index]);
          });
    });

    it('should not show the update & delete button', function(){
        var buttonUpdate = element(by.buttonText('Update Project'));
        var buttonDelete = element(by.buttonText('Delete Project'));
        expect(buttonUpdate.isDisplayed()).toBeFalsy();
        expect(buttonDelete.isDisplayed()).toBeFalsy();
    });

});

describe('testing the Project Link for user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'GET'
                },
                response: {
                    data: {
                        "owner": "thuva4",
                        "_id": "5a0c022f9a07c846d3c2cc94",
                        "creation_date": "2017-11-15 14:30:31.200259",
                        "description": "dsfsd",
                        "name": "testproject"
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/projects/testproject1',
                    method: 'GET'
                },
                response: {
                    data: {
                        "owner": "thuva4",
                        "_id": "5a0c022f9a07c846d3c2cc94",
                        "creation_date": "2017-11-15 14:30:31.200259",
                        "description": "dsfsd",
                        "name": "testproject1"
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/projects',
                    method: 'GET'
                },
                response: {
                    data: {
                        "projects": [
                            {
                            "owner": "thuva4",
                            "_id": "5a0c022f9a07c846d3c2cc94",
                            "creation_date": "2017-11-15 14:30:31.200259",
                            "description": "dsfsd",
                            "name": "testproject"
                            }
                        ]
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'DELETE'
                },
                response: {
                    status : 200
                }
            },
            {
                request: {
                    path: '/api/v1/projects/testproject1',
                    method: 'DELETE'
                },
                response: {
                    status : 403
                }
            },
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'PUT',
                    data: {
                        name: 'testProject2',
                        description : 'demoDescription',
                    }
                },
                response: {
                    status : 200,
                    data : {
                        "owner": "thuva4",
                        "_id": "5a0c022f9a07c846d3c2cc94",
                        "creation_date": "2017-11-15 14:30:31.200259",
                        "description": "dsfsd",
                        "name": "testproject2"
                    }
                }
            },
            {
                request: {
                    path: '/api/v1/projects/testproject',
                    method: 'PUT',
                    data: {
                        name: 'testProject1',
                        description : 'demoDescription',
                    }
                },
                response: {
                    status : 403
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
                        "user": "testUser", "groups": ["opnfv-testapi-users",
                        "opnfv-gerrit-testProject-submitters",
                        "opnfv-gerrit-testProject2-submitters" ],
                        "email": "testuser@test.com"
                    }
                }
            },
        ]);
    });

    afterEach(function(){
		mock.teardown();
	});

    it( 'navigate to the project page', function() {
		browser.get(baseURL+"projects/testproject");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ 'projects/testproject'), 10000);
    });

    it('show the project details for anonymous user ', function(){
        var table = $$('.projects-table.ng-scope tr');
        var projectDetailsLable = ['Name','Description','Creation date']
        var projectDetails = ['testproject', 'dsfsd','2017-11-15 14:30:31.200259']
        table.each(function(row,index) {
            var rowElems = row.$$('td');
            expect(rowElems.count()).toBe(2);
            expect(rowElems.get(0).getText()).toMatch(projectDetailsLable[index]);
            expect(rowElems.get(1).getText()).toMatch(projectDetails[index]);
          });
    });

    it('should show the update & delete button', function(){
        var buttonUpdate = element(by.buttonText('Update Project'));
        var buttonDelete = element(by.buttonText('Delete Project'));
        expect(buttonUpdate.isDisplayed()).toBe(true);
        expect(buttonDelete.isDisplayed()).toBe(true);
    });

    it('show the update modal when user clicks the update button', function(){
        browser.get(baseURL+"projects/testproject");
        var buttonDelete = element(by.buttonText('Update Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "Update"), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var buttonCancel = element(by.buttonText('Cancel')).click();
        expect(elm.isPresent()).toEqual(false);
    });

    it('send a update request to server and show success when we click ok', function(){
        browser.get(baseURL+"projects/testproject");
        var buttonUpdate = element(by.buttonText('Update Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "Update"), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var name = element(by.model('updateModal.name'));
        var description = element(by.model('updateModal.description'));
        name.click().clear().sendKeys('testProject2');
        description.click().clear().sendKeys('demoDescription');
        var buttonOk = element(by.buttonText('Ok')).click();
        expect(element(by.cssContainingText(".alert.alert-success",
                "Update Success"))
                .isDisplayed()).toBe(true);
    });

    it('show error when server send a error response when we click ok', function(){
        browser.get(baseURL+"projects/testproject");
        var buttonUpdate = element(by.buttonText('Update Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "Update"), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var name = element(by.model('updateModal.name'));
        var description = element(by.model('updateModal.description'));
        name.click().clear().sendKeys('testProject1');
        description.click().clear().sendKeys('demoDescription');
        var buttonOk = element(by.buttonText('Ok')).click();
        expect(element(by.cssContainingText(".alert",
                "Error updating the existing Project from server: undefined"))
                .isDisplayed()).toBe(true);
    });

    it('show the confirm modal when user clicks the delete button', function(){
        var buttonDelete = element(by.buttonText('Delete Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "You are about to delete."), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var buttonCancel = element(by.buttonText('Cancel')).click();
        expect(elm.isPresent()).toEqual(false);
    });

    it('send a delete request to server when we click ok', function(){
        var buttonDelete = element(by.buttonText('Delete Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "You are about to delete."), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var buttonCancel = element(by.buttonText('Ok')).click();
        browser.wait(EC.urlContains(baseURL+ 'projects'), 10000);
    });

    it('show the error message when we click ok', function(){
        browser.get(baseURL+"projects/testproject1");
        var buttonDelete = element(by.buttonText('Delete Project')).click();
        var EC = protractor.ExpectedConditions;
        var elm = element(by.css(".modal-body"));
        browser.wait(EC.textToBePresentInElement(elm, "You are about to delete."), 5000);
        expect(elm.isDisplayed()).toBe(true);
        var buttonCancel = element(by.buttonText('Ok')).click();
        // browser.wait(EC.urlContains(baseURL+ 'projects'), 10000);
        expect(element(by.cssContainingText(".alert",
        "Error deleting project from server: undefined"))
        .isDisplayed()).toBe(true);
        // browser.pause();
    });

});