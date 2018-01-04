/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

(function () {
    'use strict';

    angular
        .module('testapiApp')
        .controller('ScenarioController', ScenarioController);

        ScenarioController.$inject = [
        '$scope', '$http', '$filter', '$state', '$window', '$uibModal', 'testapiApiUrl','raiseAlert',
        'confirmModal'
    ];

    /**
     * TestAPI Scenario Controller
     * This controller is for the '/Scenario/:name' page where a user can browse
     * through Scenario declared in TestAPI.
     */
    function ScenarioController($scope, $http, $filter, $state, $window, $uibModal, testapiApiUrl,
        raiseAlert, confirmModal) {
        var ctrl = this;
        ctrl.name = $state.params['name'];
        ctrl.url = testapiApiUrl + '/scenarios?name=' + ctrl.name;
        ctrl.expandInstallers = expandInstallers;
        ctrl.expandInstaller = expandInstaller;
        ctrl.expandInstaller = ctrl.expandInstaller;
        ctrl.expandVersion = expandVersion;
        ctrl.expandVersions = expandVersions;
        ctrl.loadDetails = loadDetails;
        ctrl.expandProjects = expandProjects
        ctrl.expandProject = expandProject
        ctrl.expandTrustIndicator = expandTrustIndicator;
        ctrl.expandScore = expandScore;
        ctrl.expandCustom = expandCustom;
        ctrl.collapeVersion = {};
        ctrl.collapeVersions = {};
        ctrl.collapeProjects = {};
        ctrl.collapeProject = {};
        ctrl.collapeTrustIndicator = {};
        ctrl.collapeScore = {};
        ctrl.collapeCustom = {};
        ctrl.collapeInstaller = {};

        /**
         * This will contact the TestAPI to get a listing of declared projects.
         */
        function loadDetails() {
            ctrl.showError = false;
            ctrl.projectsRequest =
                $http.get(ctrl.url).success(function (data) {
                    ctrl.data = data;
                }).catch(function (error) {
                    ctrl.data = null;
                    ctrl.showError = true;
                    ctrl.error = error.statusText
                });
        }

        function expandTrustIndicator(index){
            if(ctrl.collapeTrustIndicator[index]){
                ctrl.collapeTrustIndicator[index] = false;
            }else{
                ctrl.collapeTrustIndicator[index] = true;
            }
        }

        function expandScore(index){
            if(ctrl.collapeScore[index]){
                ctrl.collapeScore[index] = false;
            }else{
                ctrl.collapeScore[index] = true;
            }
        }

        function expandCustom(index){
            if(ctrl.collapeCustom[index]){
                ctrl.collapeCustom[index] = false;
            }else{
                ctrl.collapeCustom[index] = true;
            }
        }

        function expandVersion(index){
            if(ctrl.collapeVersion[index]){
                ctrl.collapeVersion[index] = false;
            }else{
                ctrl.collapeVersion[index] = true;
            }
        }

        function expandVersions(index){
            if(ctrl.collapeVersions[index]){
                ctrl.collapeVersions[index] = false;
            }else{
                ctrl.collapeVersions[index] = true;
            }
        }

        function expandProjects(index){
            if(ctrl.collapeProjects[index]){
                ctrl.collapeProjects[index] = false;
            }
            else{
                ctrl.collapeProjects[index]= true;
            }
        }

        function expandProject(index){
            if(ctrl.collapeProject[index]){
                ctrl.collapeProject[index] = false;
            }
            else{
                ctrl.collapeProject[index]= true;
            }
        }

        function expandInstaller(index){
            if(ctrl.collapeInstaller[index]){
                ctrl.collapeInstaller[index] = false;
            }
            else{
                ctrl.collapeInstaller[index]= true;
            }
        }

        function expandInstallers(){
            if(ctrl.collapeInstallers){
                ctrl.collapeInstallers= false
            }else{
                ctrl.collapeInstallers= true
            }
        }
        ctrl.loadDetails();
    }
})();
