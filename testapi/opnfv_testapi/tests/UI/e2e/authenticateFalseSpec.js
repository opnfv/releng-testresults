
var mock = require('protractor-http-mock');
var baseURL = "http://localhost:8000/";


describe('testing the pods page for anonymous user', function () {
    beforeEach(function(){
        mock([{
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
        }
        ]);
    });

    afterEach(function(){
        mock.teardown();
    });

    it('Delete button is visible for  anonymous user', function () {
        var fs = require('fs')
        var m = JSON.parse(fs.readFileSync('testapi-ui/config.json').toString());
        m.authenticate = false;
        fs.writeFile('testapi-ui/config.json', JSON.stringify(m, null, 2))
        browser.restart();
        browser.get(baseURL+'#/pods');
        var buttonDelete = element(by.buttonText('Delete'));
        expect(buttonDelete.isDisplayed()).toBe(true)
    });

    it('Delete button is visible for anonymous  user', function () {
        var buttonDelete = element(by.buttonText('Delete'));
        expect(buttonDelete.isDisplayed()).toBe(true)
    });

    it('delete Operation is  visible for  user ', function () {
        var deleteOperation = element(by.css('a[title=Delete]'));
        expect(deleteOperation.isDisplayed()).toBe(true);
    });
});

describe('testing the pods page for anonymous user', function () {
    beforeEach(function(){
        mock([
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
            }
        ]);
    });

    afterEach(function(){
        mock.teardown();
    });

    it('create button is visible for user', function () {
        browser.get(baseURL+'#/projects');
        var buttonCreate = element(by.buttonText('Create'));
        expect(buttonCreate.isDisplayed()).toBe(true);
    });

    it('delete Operation is visible for  user ', function () {
        browser.get(baseURL+'#/projects');
        var deleteOperation = element(by.css('a[title=Delete]'));
        expect(deleteOperation.isDisplayed()).toBe(true);
    });

    it('Edit Operation is visible for  user ', function () {
        browser.get(baseURL+'#/projects');
        var editOperation = element(by.css('a[title=Edit]'));
        expect(editOperation.isDisplayed()).toBe(true);
    });
});


describe('testing the scenarios page for anonymous user', function () {
    beforeEach(function(){
        mock([
            {
                request: {
                    path: '/api/v1/scenarios',
                    method: 'GET'
                },
                response: {
                    data: {
                        "scenarios": [
                            {
                            "installers": [
                               {
                                  "installer": "fuel",
                                  "versions": [
                                     {
                                        "owner": "testUser",
                                        "version": "colorado",
                                        "projects": [
                                           {
                                              "project": "yardstick",
                                              "customs": [
                                                 "dvs"
                                              ],
                                              "scores": [
                                                 {
                                                    "date": "2016-12-11 01:45",
                                                    "score": "14/24"
                                                 }
                                              ],
                                              "trust_indicators": [
                                                 {
                                                    "date": "2016-12-09 11:38",
                                                    "status": "silver"
                                                 }
                                              ]
                                           },
                                           {
                                              "project": "functest",
                                              "customs": [
                                                 "vping_ssh",
                                                 "vping_userdata",
                                              ],
                                              "scores": [
                                                 {
                                                    "date": "2016-12-09 11:28",
                                                    "score": "6/8"
                                                 }
                                              ],
                                              "trust_indicators": [
                                                 {
                                                    "date": "2016-12-09 11:38",
                                                    "status": "silver"
                                                 }
                                              ]
                                           },
                                           {
                                              "project": "sla",
                                              "customs": [],
                                              "scores": [
                                                 {
                                                    "date": "2018-01-16T18:30:00.000Z",
                                                    "score": "sdS"
                                                 }
                                              ],
                                              "trust_indicators": []
                                           },
                                           {
                                              "project": "dvsd",
                                              "customs": [],
                                              "scores": [],
                                              "trust_indicators": []
                                           }
                                        ]
                                     },
                                     {
                                        "owner": "dfgvds",
                                        "version": "df",
                                        "projects": []
                                     }
                                  ]
                               },
                               {
                                  "installer": "fuel2",
                                  "versions": [
                                     {
                                        "owner": "testUser",
                                        "version": "colorado",
                                        "projects": [
                                           {
                                              "project": "yardstick",
                                              "customs": [
                                                 "tc002",
                                                 "tc005",
                                                 "tc010",
                                                 "tc011"
                                              ],
                                              "scores": [
                                                 {
                                                    "date": "2016-12-11 01:45",
                                                    "score": "14/24"
                                                 }
                                              ],
                                              "trust_indicators": [
                                                 {
                                                    "date": "2016-12-09 11:38",
                                                    "status": "silver"
                                                 }
                                              ]
                                           },
                                           {
                                              "project": "functest",
                                              "customs": [
                                                 "vping_ssh",
                                                 "vping_userdata"
                                              ],
                                              "scores": [
                                                 {
                                                    "date": "2016-12-09 11:28",
                                                    "score": "6/8"
                                                 }
                                              ],
                                              "trust_indicators": [
                                                 {
                                                    "date": "2016-12-09 11:38",
                                                    "status": "silver"
                                                 }
                                              ]
                                           }
                                        ]
                                     }
                                  ]
                               }
                            ],
                            "_id": "5a50fcacsdgdsgdasgfvb861c",
                            "name": "test-scenario",
                            "creation_date": "2018-01-06 22:13:24.160407"
                            }
                        ]
                    }
                }
            }
        ])
    });

    afterEach(function(){
        mock.teardown();
    });

    it( 'should show the add installer option for anonymous user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var buttonAdd = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[2]/button'))
        expect(buttonAdd.isDisplayed()).toBe(true);
    });

    it( 'should show the delete installer option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerDelete = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[3]/button'))
        expect(installerDelete.isDisplayed()).toBe(true);
    });

    it( 'should show the add version option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionAdd = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[2]/button'))
        versionAdd.click()
        expect(versionAdd.isDisplayed()).toBe(true);
    });

    it( 'should show the delete version option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[1]/a/p'))
        versionsShow.click();
        var versionShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        versionShow.click()
        var versionDelete = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody[1]/tr[1]/td[3]/button'))
        expect(versionDelete.isDisplayed()).toBe(true);
    });

    it( 'should show the add project option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[1]/a/p'))
        versionsShow.click();
        var versionShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        versionShow.click()
        var projectAdd = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[2]/button'))
        projectAdd.click()
        expect(projectAdd.isDisplayed()).toBe(true);
    });

    it( 'should show the delete project option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[1]/a/p'))
        versionsShow.click();
        var versionShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        versionShow.click()
        var projectsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[1]/a'))
        projectsShow.click();
        var projectDelete = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody[1]/tr[1]/td[3]/button'))
        projectDelete.click()
        expect(projectDelete.isDisplayed()).toBe(true);
    });

    it( 'should show the add customs option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[1]/a/p'))
        versionsShow.click();
        var versionShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        versionShow.click()
        var projectsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[1]/a'))
        projectsShow.click();
        var projectShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        projectShow.click();
        var customsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody[1]/tr[4]/td[2]/a/p'))
        customsShow.click();
        var row = element.all(by.repeater('(indexCU, custom) in project.customs')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("dvs");
        var buttonAdd = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody[1]/tr[4]/td[2]/button'))
        buttonAdd.click()
        expect(buttonAdd.isDisplayed()).toBe(true);
    });

    it( 'should show the delete customs option for  user', function() {
        browser.get(baseURL+"#/scenarios/test-scenario");
        var EC = browser.ExpectedConditions;
        browser.wait(EC.urlContains(baseURL+ '#/scenarios/test-scenario'), 10000);
        var installersShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[1]/a/p'))
        installersShow.click();
        var installerShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        installerShow.click();
        var versionsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[1]/a/p'))
        versionsShow.click();
        var versionShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        versionShow.click()
        var projectsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[1]/a'))
        projectsShow.click();
        var projectShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody/tr[1]/td[2]/a'))
        projectShow.click();
        var customsShow = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody[1]/tr[4]/td[2]/a/p'))
        customsShow.click();
        var row = element.all(by.repeater('(indexCU, custom) in project.customs')).first();
        var cells = row.all(by.tagName('td'));
        expect(cells.get(0).getText()).toContain("dvs");
        var buttonDelete = element(by.xpath('//*[@id="ng-app"]/body/div/div[1]/div/table/tbody/tr[4]/td[2]/div[3]/div/table/tbody/tr[2]/td[2]/div[3]/div/table/tbody/tr[3]/td[2]/div[3]/div/table/tbody[1]/tr[4]/td[2]/table/tbody/tr[1]/td[2]/button'))
        buttonDelete.click()
        expect(buttonDelete.isDisplayed()).toBe(true);
    });
});


