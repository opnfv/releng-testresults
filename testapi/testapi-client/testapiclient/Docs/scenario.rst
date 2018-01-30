scenario get

scenario create -scenario '{ "installers": [], "name": "os-Fake-ha"}'

scenario delete -name scenarioName

scenario getOne -name scenarioName

scenario put -name scenarioName -scenario '{ "installers": [], "name": "os-Fake-ha"}'




scenario addScore -scenario scenarioName -installer installerName -version versionName -project projectName -score '{"date": "2018-01-17T18:30:00.000Z", "score": "score"}'

scenario addTI -scenario scenarioName -installer installerName -version versionName -project projectName -ti '{"date": "2018-01-17T18:30:00.000Z", "status": "silver"}'


scenario addCustom -scenario scenarioName -installer installerName -version versionName -project projectName -custom '["asf","saf"]'

scenario updateCustom -scenario scenarioName -installer installerName -version versionName -project projectName -custom '["fdsg","adf"]'

scenario deleteCustom -scenario scenarioName -installer installerName -version versionName -project projectName -custom '["fdsg","adf"]'




scenario addProject -scenario scenarioName -installer installerName -version versionName -project '{"project": "Project1","customs": ["sfgvf"],"scores": [{"date": "2018-01-30T18:30:00.000Z","score": "10/19"}],"trust_indicators": []}'

scenario deleteProject -scenario scenarioName -installer installerName -version versionName -project projectName


scenario addVersion -scenario scenarioName -installer installerName -version '{"owner": null,"version": "version1","projects": [{"project": "","customs": [],"scores": [],"trust_indicators": []}]}]}'

scenario deleteVersion -scenario scenarioName -installer installerName -version versionName


scenario addInstaller -scenario scenarioName -installer ' {"installer": "installer1","versions": []}'

scenario deleteInstaller -scenario scenarioName -installer installerName