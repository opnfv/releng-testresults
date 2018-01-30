

project create -project '{ "name": "demoProject", "description": "demo description"}'

project get

project get -name demoProject

project getOne -name demoProject

project delete -name demoProject

project put -name demoProject -project '{ "name": "demoProject", "description": "updated demo description"}'
