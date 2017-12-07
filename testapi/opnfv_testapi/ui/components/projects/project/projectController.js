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
        ctrl.url = testapiApiUrl + '/projects/' + ctrl.name;

        ctrl.loadDetails = loadDetails;
        ctrl.deleteProject = deleteProject;
        ctrl.openDeleteModal = openDeleteModal;
        ctrl.openUpdateModal = openUpdateModal;
        ctrl.updateProject = updateProject;

        /**
         * This will contact the TestAPI to update an existing project.
         */
        function updateProject(name,project) {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            var projects_url = ctrl.url;
            var body = {
                name: project.name,
                description: project.description
            };
            ctrl.projectsRequest =
                $http.put(projects_url, body).success(function (data){
                    ctrl.showSuccess = true ;
                    ctrl.name = body.name;
                    $state.go('project', {'name':ctrl.name}, {reload: true});
                })
                .catch(function (error) {
                    ctrl.showError = true;
                    ctrl.error = error.statusText
                });


        }

        /**
         * This will contact the TestAPI to delete an existing project.
        */
        function deleteProject() {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            ctrl.projectsRequest =
            $http.delete(ctrl.url).success(function (data) {
                $state.go('projects', {'name':ctrl.name}, {reload: true});
                ctrl.showSuccess = true ;
            }).catch(function (error) {
                ctrl.showError = true;
                ctrl.error = error.statusText
            });
        }

        /**
         * This will open the modal that will show the delete confirm
         * message
         */
        function openDeleteModal() {
            confirmModal("Delete",ctrl.deleteProject);
        }

        /**
         * This will open the modal that will show the update
         * view
         */
        function openUpdateModal(){
                $uibModal.open({
                    templateUrl: 'testapi-ui/components/projects/modals/projectModal.html',
                    controller: 'ProjectModalCtrl as ProjectModalCtrl',
                    size: 'md',
                    resolve: {
                        data: function () {
                            return {
                                text: "Update Project",
                                successHandler: ctrl.updateProject,
                                project : ctrl.data
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
                $http.get(ctrl.url).success(function (data) {
                    ctrl.data = data;
                }).catch(function (error) {
                    ctrl.data = null;
                    ctrl.showError = true;
                    ctrl.error = error.statusText
                });
        }
        ctrl.loadDetails();
    }
})();
