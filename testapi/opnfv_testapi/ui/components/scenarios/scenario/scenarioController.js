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
        ctrl.addCustom = addCustom;
        ctrl.openAddCustomModal = openAddCustomModal;
        ctrl.openAddTrustIndicatorModal = openAddTrustIndicatorModal;
        ctrl.addTrustindicator = addTrustindicator;
        ctrl.addScore = addScore;
        ctrl.openAddScoreModal = openAddScoreModal;
        ctrl.openDeleteCustomModal = openDeleteCustomModal;
        ctrl.deleteCustom = deleteCustom;
        ctrl.addProject = addProject
        ctrl.openAddProjectModal = openAddProjectModal
        ctrl.openAddVersionModal = openAddVersionModal
        ctrl.addVersion = addVersion
        ctrl.openDeleteVersionModal = openDeleteVersionModal
        ctrl.deleteVersion = deleteVersion
        ctrl.openAddInstaller = openAddInstaller
        ctrl.addInstaller = addInstaller
        ctrl.openDeleteInstallerModal = openDeleteInstallerModal
        ctrl.deleteInstaller = deleteInstaller

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

        function deleteInstaller(data){
            ctrl.installerReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/installers"
            $http.delete(ctrl.installerReqest, {data: data.installers, headers: {'Content-Type': 'application/json'}}).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Installer is successfully deleted."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openDeleteInstallerModal(installer){
            var installers = []
            installers.push(installer)
            var data = {
                "installers": installers
            }
            confirmModal("Delete",ctrl.deleteInstaller,data);
        }

        function addInstaller(installer){
            var installers = []
            installers.push(installer)
            ctrl.installerReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/installers"
            $http.post(ctrl.installerReqest, installers).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Installers are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openAddInstaller(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/installerModal.html',
                controller: 'installerModalCtrl as installerModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Installer",
                            successHandler: ctrl.addInstaller
                        };
                    }
                }
            });
        }

        function addVersion(versions, installer){
            ctrl.versionReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/versions?installer="+installer
            $http.post(ctrl.versionReqest, versions).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Versions are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openDeleteVersionModal(version, installer){
            var versions = []
            versions.push(version)
            var data = {
                "version": versions,
                "installer": installer
            }
            confirmModal("Delete",ctrl.deleteVersion,data);
        }

        function deleteVersion(data){
            ctrl.versionReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/versions?installer="+data.installer
            $http.delete(ctrl.versionReqest, {data: data.version, headers: {'Content-Type': 'application/json'}}).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Versions are successfully deleted."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openAddVersionModal(installer){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/versionModal.html',
                controller: 'versionAddModalCtrl as versionModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Version",
                            successHandler: ctrl.addVersion,
                            installer: installer
                        };
                    }
                }
            });
        }

        function addProject(project, version, installer){
            ctrl.projectReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/projects?installer="+installer+"&version="+version
            $http.post(ctrl.projectReqest, project).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Projects are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openAddProjectModal(version, installer){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/projectModal.html',
                controller: 'projectAddModalCtrl as projectModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Project",
                            successHandler: ctrl.addProject,
                            version: version,
                            installer: installer
                        };
                    }
                }
            });
        }

        function addCustom(custom,project,version,installer){
            ctrl.customReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/customs?installer="+installer+"&version="+version+"&project="+ project
            $http.post(ctrl.customReqest, custom).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Customs are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openDeleteCustomModal(custom,project,version,installer){
            var customs = []
            customs.push(custom)
            var data = {
                "customs": customs,
                "project": project,
                "version": version,
                "installer": installer
            }
            confirmModal("Delete",ctrl.deleteCustom,data);
        }

        function deleteCustom(data){
            ctrl.customReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/customs?installer="+data.installer+"&version="+data.version+"&project="+ data.project
            $http.delete(ctrl.customReqest, {data: data.customs, headers: {'Content-Type': 'application/json'}}).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Customs are successfully deleted."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function openAddCustomModal(project,version,installer){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/customModal.html',
                controller: 'customAddModalCtrl as customModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Custom",
                            successHandler: ctrl.addCustom,
                            project: project,
                            version: version,
                            installer: installer
                        };
                    }
                }
            });
        }

        function openAddTrustIndicatorModal(project, version, installer){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/trustIndicatorModal.html',
                controller: 'trustIndicatorAddModalCtrl as trustIndicatorModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Trust Indicator",
                            successHandler: ctrl.addTrustindicator,
                            project: project,
                            version: version,
                            installer: installer
                        };
                    }
                }
            });
        }

        function openAddScoreModal(project, version, installer){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/scoreModal.html',
                controller: 'scoreAddModalCtrl as scoreModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Add Score",
                            successHandler: ctrl.addScore,
                            project: project,
                            version: version,
                            installer: installer
                        };
                    }
                }
            });
        }

        function addTrustindicator(trust_indicator, project, version, installer){
            ctrl.customReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/trust_indicators?installer="+installer+"&version="+version+"&project="+ project
            $http.post(ctrl.customReqest,trust_indicator ).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Trust indicators are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        function addScore(score, project, version, installer){
            ctrl.customReqest = testapiApiUrl+ "/scenarios/"+ ctrl.name + "/scores?installer="+installer+"&version="+version+"&project="+ project
            $http.post(ctrl.customReqest,score ).success(function (data){
                ctrl.showSuccess = true ;
                ctrl.success = "Scores are successfully updated."
                ctrl.loadDetails();
            })
            .catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        ctrl.loadDetails();
    }

     /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
     */
    angular.module('testapiApp').controller('customAddModalCtrl', customAddModalCtrl);
    customAddModalCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function customAddModalCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.open = open;


        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            ctrl.customs = []
            ctrl.customs.push(ctrl.custom)
            ctrl.data.successHandler(ctrl.customs,ctrl.data.project,ctrl.data.version,ctrl.data.installer);
            $uibModalInstance.dismiss('cancel');

        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }
    }

    /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
     */
    angular.module('testapiApp').controller('trustIndicatorAddModalCtrl', trustIndicatorAddModalCtrl);
    trustIndicatorAddModalCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function trustIndicatorAddModalCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.open = open;


        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            ctrl.data.successHandler(ctrl.ti, ctrl.data.project, ctrl.data.version, ctrl.data.installer);
            $uibModalInstance.dismiss('cancel');

        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }

        function handleModalData(){

        }

        /**
         * This is called when the date filter calendar is opened. It
         * does some event handling, and sets a scope variable so the UI
         * knows which calendar was opened.
         * @param {Object} $event - The Event object
         * @param {String} openVar - Tells which calendar was opened
         */
        function open($event, openVar) {
            $event.preventDefault();
            $event.stopPropagation();
            ctrl[openVar] = true;
        }
    }

        /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
     */
    angular.module('testapiApp').controller('scoreAddModalCtrl', scoreAddModalCtrl);
    scoreAddModalCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function scoreAddModalCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.open = open;

        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            ctrl.data.successHandler(ctrl.score, ctrl.data.project, ctrl.data.version, ctrl.data.installer);
            $uibModalInstance.dismiss('cancel');
        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }

        function handleModalData(){

        }

        /**
         * This is called when the date filter calendar is opened. It
         * does some event handling, and sets a scope variable so the UI
         * knows which calendar was opened.
         * @param {Object} $event - The Event object
         * @param {String} openVar - Tells which calendar was opened
         */
        function open($event, openVar) {
            $event.preventDefault();
            $event.stopPropagation();
            ctrl[openVar] = true;
        }
    }

     /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
    */
    angular.module('testapiApp').controller('projectAddModalCtrl', projectAddModalCtrl);
    projectAddModalCtrl.$inject = ['$scope', '$uibModal', '$uibModalInstance', 'data'];
    function projectAddModalCtrl($scope, $uibModal, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.openScoreModal = openScoreModal;
        ctrl.openTrustIndicatorModal = openTrustIndicatorModal;
        ctrl.openCustomModal = openCustomModal;
        ctrl.handleScore = handleScore;
        ctrl.handleModalTrustIndicator = handleModalTrustIndicator;
        ctrl.handleModalCustom = handleModalCustom;
        ctrl.projects = []
        ctrl.project = {
            "scores": [],
            "trust_indicators": [],
            "customs": []
        }


        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            ctrl.projects.push(ctrl.project)
            ctrl.data.successHandler(ctrl.projects, ctrl.data.version, ctrl.data.installer);
            $uibModalInstance.dismiss('cancel');

        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }

        function handleModalTrustIndicator(trustIndicator){
            ctrl.project.trust_indicators.push(trustIndicator)
        }

        function handleScore(score){
            ctrl.project.scores.push(score);
        }

        function handleModalCustom(custom){
            ctrl.project.customs.push(custom);
        }

        function openScoreModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/scoreModal.html',
                controller: 'scoreModalCtrl as scoreModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Score",
                            successHandler: ctrl.handleScore,
                        };
                    }
                }
            });
        }
        function openTrustIndicatorModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/trustIndicatorModal.html',
                controller: 'trustIndicatorModalCtrl as trustIndicatorModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Trust Indicator",
                            successHandler: ctrl.handleModalTrustIndicator
                        };
                    }
                }
            });
        }
        function openCustomModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/customModal.html',
                controller: 'customModalCtrl as customModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Custom",
                            successHandler: ctrl.handleModalCustom
                        };
                    }
                }
            });
        }
    }

        /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
    */
    angular.module('testapiApp').controller('versionAddModalCtrl', versionAddModalCtrl);
    versionAddModalCtrl.$inject = ['$scope', '$uibModal','$uibModalInstance', 'data'];
    function versionAddModalCtrl($scope, $uibModal, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.openProjectModal = openProjectModal;
        ctrl.handleModalData = handleModalData;
        ctrl.versions = []
        ctrl.version = {
            "projects": []
        }

        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            ctrl.versions.push(ctrl.version)
            ctrl.data.successHandler(ctrl.versions, ctrl.data.installer);
            $uibModalInstance.dismiss('cancel');

        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }

        function handleModalData(project){
            ctrl.version.projects.push(project)
        }
        function openProjectModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/scenarios/modals/projectModal.html',
                controller: 'projectModalCtrl as projectModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Project",
                            successHandler: ctrl.handleModalData,
                        };
                    }
                }
            });
        }
    }

})();
