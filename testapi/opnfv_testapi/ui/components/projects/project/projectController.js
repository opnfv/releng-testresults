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
        .controller('ProjectController', ProjectController);

        ProjectController.$inject = [
        '$scope', '$http', '$filter', '$state', '$window', '$uibModal', 'testapiApiUrl','raiseAlert',
        'confirmModal'
    ];

    /**
     * TestAPI Project Controller
     * This controller is for the '/projects' page where a user can browse
     * through projects declared in TestAPI.
     */
    function ProjectController($scope, $http, $filter, $state, $window, $uibModal, testapiApiUrl,
        raiseAlert, confirmModal) {
        var ctrl = this;
        ctrl.name = $state.params['name'];
        ctrl.url = testapiApiUrl + '/projects/' ;

        ctrl.loadDetails = loadDetails;
        ctrl.deleteProject = deleteProject;
        ctrl.openDeleteModal = openDeleteModal;
        ctrl.openUpdateModal = openUpdateModal;
        ctrl.updateProject = updateProject;


        /**
         * This will contact the TestAPI to update an existing project.
         */
        function updateProject(name,description) {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            if(ctrl.name != ""){
                var projects_url = ctrl.url + ctrl.name;
                var body = {
                    name: name,
                    description: description
                };
                ctrl.projectsRequest =
                    $http.put(projects_url, body).success(function (data){
                        $state.go('project', { name : body.name })
                    })
                    .catch(function (data) {
                        ctrl.showError = true;
                        ctrl.error = data.statusText;
                    });

            }
            else{
                ctrl.showError = true;
                ctrl.error = 'Name is missing.'
            }
        }

        /**
         * This will contact the TestAPI to delete an existing project.
        */
        function deleteProject() {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            ctrl.projectsRequest =
            $http.delete(ctrl.url + ctrl.name).success(function (data) {
                $state.go('projects', {}, {reload: true});

            }).catch(function (data) {
                ctrl.showError = true;
                ctrl.error = data.statusText;
            });
        }

        /**
         * This will open the modal that will show the delete confirm
         * message
         */
        function openDeleteModal() {
            confirmModal("Delete", ctrl.deleteProject, null);
        }

        /**
         * This will open the modal that will show the update
         * view
         */
        function openUpdateModal(){
                $uibModal.open({
                    templateUrl: 'testapi-ui/components/projects/project/updateModal.html',
                    controller: 'TestModalInstanceCtrl as updateModal',
                    size: 'md',
                    resolve: {
                        data: function () {
                            return {
                                text: "Update",
                                successHandler: ctrl.updateProject,
                                project: ctrl.data
                            };
                        }
                    }
                });
        }

        /**
         * This will contact the TestAPI to get a listing of declared projects.
         */
        function loadDetails() {
            ctrl.showError = false;
            ctrl.projectsRequest =
                $http.get(ctrl.url + ctrl.name).success(function (data) {
                    ctrl.data = data;
                }).catch(function (data) {
                    ctrl.data = null;
                    ctrl.showError = true;
                    ctrl.error = data.statusText;
                });
        }
        ctrl.loadDetails();
    }


    /**
     * TestAPI Modal instance Controller
     * This controller is for the update modal where a user can update
     * the project information.
     */
    angular.module('testapiApp').controller('TestModalInstanceCtrl', TestModalInstanceCtrl);
    TestModalInstanceCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function TestModalInstanceCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);

        ctrl.createRequirements = [
            {label: 'name', type: 'text', required: true},
            {label: 'description', type: 'textarea', required: false}
        ];

        ctrl.name = ctrl.data.project.name;
        ctrl.description = ctrl.data.project.description;

        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            $uibModalInstance.close();
            if (angular.isDefined(ctrl.data.successHandler)) {
                ctrl.data.successHandler(ctrl.name,ctrl.description);
            }
        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }
    }


})();
