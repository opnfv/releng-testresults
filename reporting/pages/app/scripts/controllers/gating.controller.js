'use strict';

angular.module('opnfvApp')
    .controller('GatingController', ['$scope', '$state', '$stateParams', 'TableFactory', function($scope, $state, $stateParams, TableFactory) {

        init();

        function init() {
            $scope.goTest = goTest;
            $scope.goLogin = goLogin;

            $scope.scenarios = {};

            $scope.scenarioList = _toSelectList(['all']);
            $scope.versionList = _toSelectList(['master', 'fraser', 'gambia']);
            $scope.installerList = _toSelectList(['all', 'apex', 'compass', 'daisy', 'fuel', 'joid']);
            $scope.iterationList = _toSelectList([10, 20, 30]);

            $scope.selectScenario = 'all';
            $scope.selectVersion = 'master';
            $scope.selectInstaller = 'all';
            $scope.selectIteration = 10;

            $scope.ScenarioConfig = {
                create: true,
                valueField: 'title',
                labelField: 'title',
                delimiter: '|',
                maxItems: 1,
                placeholder: 'Scenario',
                onChange: function(value) {
                    $scope.selectScenario = value;
                }
            }

            $scope.VersionConfig = {
                create: true,
                valueField: 'title',
                labelField: 'title',
                delimiter: '|',
                maxItems: 1,
                placeholder: 'Version',
                onChange: function(value) {
                    $scope.selectVersion = value;
                    getScenarioResult();
                }
            }

            $scope.InstallerConfig = {
                create: true,
                valueField: 'title',
                labelField: 'title',
                delimiter: '|',
                maxItems: 1,
                placeholder: 'Installer',
                onChange: function(value) {
                    $scope.selectInstaller = value;
                    getScenarioResult();
                }
            }

            $scope.IterationConfig = {
                create: true,
                valueField: 'title',
                labelField: 'title',
                delimiter: '|',
                maxItems: 1,
                placeholder: 'Iteration',
                onChange: function(value) {
                    $scope.selectIteration = value;
                    getScenarioResult();
                }
            }
            getScenarioResult();
        }

        function getScenarioResult(){
            _getScenarioResult($scope.selectVersion, $scope.selectInstaller, $scope.selectIteration);
        }

        function _getScenarioResult(version, installer, iteration){
            var data = {
                'version': version,
                'iteration': iteration
            }

            if(installer != 'all'){
                data['installer'] = installer;
            }

            TableFactory.getScenarioResult().get(data).$promise.then(function(resp){
                $scope.scenarios = resp;
                _concat($scope.scenarioList, _toSelectList(Object.keys(resp)));
            }, function(err){
            });
        }

        function _concat(aList, bList){
            angular.forEach(bList, function(ele){
                aList.push(ele);
            });
        }

        function _toSelectList(arr){
            var tempList = [];
            angular.forEach(arr, function(ele){
                tempList.push({'title': ele});
            });
            return tempList;
        }

        function goTest() {
            $state.go("select.selectTestCase");
        }

        function goLogin() {
            $state.go("login");
        }
    }]);
