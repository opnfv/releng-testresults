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
        .controller('ProjectsController', ProjectsController);

        ProjectsController.$inject = [
        '$scope', '$http', '$filter', '$state', '$window', '$uibModal', 'testapiApiUrl',
        'raiseAlert', 'confirmModal', 'authenticate', 'keepState', 'sortService', '$timeout'
    ];

    /**
     * TestAPI Project Controller
     * This controller is for the '/projects' page where a user can browse
     * through projects declared in TestAPI.
     */
    function ProjectsController($scope, $http, $filter, $state, $window, $uibModal, testapiApiUrl,
        raiseAlert, confirmModal, authenticate, keepState, sortService, $timeout) {
        var ctrl = this;
        ctrl.url = testapiApiUrl + '/projects';

        ctrl.create = create;
        ctrl.listProjects = listProjects;
        ctrl.openCreateModal = openCreateModal;
        ctrl.viewProject = viewProject;
        ctrl.openUpdateModal = openUpdateModal;
        ctrl.update = update;
        ctrl.openDeleteModal = openDeleteModal;
        ctrl.openBatchDeleteModal = openBatchDeleteModal;
        ctrl.projectDelete = projectDelete;
        ctrl.batchDelete = batchDelete;
        ctrl.sortByName = sortByName

        ctrl.checkBox = [];
        ctrl.checkBoxList = [];
        ctrl.name = '';
        ctrl.details = '';
        ctrl.ascending = false;
        ctrl.toastError = toastError
        ctrl.toastSuccess = toastSuccess

        function toastError() {
            ctrl.showError = true
            $timeout(function(){ ctrl.showError = false;}, 7000);
        }

        function toastSuccess() {
            ctrl.showSuccess = true
            $timeout(function(){ ctrl.showSuccess = false;}, 7000);
        }

        /**
         * This will contact the TestAPI to create a new project.
         */
        function create(project) {
            var projects_url = ctrl.url;
            var body = {
                name: project.name,
                description: project.description
            };
            ctrl.projectsRequest = $http.post(projects_url, body)
            ctrl.projectsRequest.success(function (data){
                    ctrl.success = "Project is successfully created.";
                    ctrl.listProjects();
                    ctrl.toastSuccess();
                    ctrl.request = true;
                }).catch(function (data) {
                    ctrl.error = data.statusText;
                    ctrl.toastError();
                    ctrl.request = false;
                });

            return ctrl.projectsRequest
        }

        function sortByName(){
            ctrl.data.projects = sortService.sortFunction(ctrl.data.projects, 'name', ctrl.ascending)
            ctrl.ascending = !ctrl.ascending
        }

        /**
         * This will open the modal that will show the create
         * project view
         */
        function openCreateModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/projects/modals/projectModal.html',
                controller: 'ProjectModalCtrl as ProjectModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Create Project",
                            successHandler: ctrl.create
                        };
                    }
                }
            });
        }

        /**
         * This will open the modal that will show the update
         * project view
         */
        function openUpdateModal(name){
            var project;
            var index;
            for(index in ctrl.data.projects){
                if(ctrl.data.projects[index].name==name){
                    project = ctrl.data.projects[index]
                    continue
                }
            }
            $uibModal.open({
                templateUrl: 'testapi-ui/components/projects/modals/projectModal.html',
                controller: 'ProjectModalCtrl as ProjectModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Update Project",
                            successHandler: ctrl.update,
                            project : project
                        };
                    }
                }
            });
        }

        /**
         * This will contact the TestAPI to update an existing test case.
         */
        function update(name, project) {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            var projectUrl = ctrl.url + '/' + name;
            ctrl.projectRequest = $http.put(projectUrl, project)
            ctrl.projectRequest.success(function (data){
                    ctrl.success = "Project is successfully updated."
                    ctrl.listProjects();
                    ctrl.toastSuccess();
                })
                .catch(function (data) {
                    ctrl.error = data.statusText;
                    ctrl.toastError();
                });
            return ctrl.projectRequest
        }

        /**
         * This will contact the TestAPI to get a listing of declared projects.
         */
        function listProjects() {
            ctrl.showError = false;
            var content_url = ctrl.url + '?';
            var filterText  = ctrl.filterText;
            if(filterText != undefined){
                content_url = content_url + 'name=' +
                filterText;
            }
            else if(keepState.filter.projectFilter){
                for (var filter in keepState.filter.projectFilter){
                    content_url = content_url + filter + '=' + keepState.filter.projectFilter[filter]
                    ctrl.filterText = keepState.filter.projectFilter[filter]
                }
            }
            ctrl.resultsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.data = data;
                    if(ctrl.filterText != undefined){
                        keepState.filter.projectFilter = {
                            'name': ctrl.filterText
                        }
                    }
                }).catch(function (data)  {
                    ctrl.data = null;
                    ctrl.error = data.statusText;
                    ctrl.toastError();
                });
        }

        function viewProject(name){
            $state.go('project', {'name':name}, {reload: true});
        }

        /**
         * This will contact the TestAPI to delete a project for given
         * name.
         */
        function projectDelete(projectName){
            var projectUrl = ctrl.url + "/" + projectName
            $http.delete(projectUrl).success(function(){
                ctrl.success = "Projects is successfully deleted"
                ctrl.toastSuccess();
                ctrl.listProjects();
            }).catch(function (data)  {
                ctrl.error = data.statusText;
                ctrl.toastError();
            });
        }

        /**
         * This will  delete list of projects.
         */
        function batchDelete(){
            var index;
            var checkedBox = [];
            ctrl.checkBox.forEach(function(project, index){
                if(!ctrl.showError){
                    if(project){
                        projectDelete(ctrl.data.projects[index].name);
                    }
                }
              });
            ctrl.checkBox = []
        }

        /**
         * This will open the modal that will show the batch delete confirm
         * message
         */
        function openBatchDeleteModal() {
            var deleteObjects = []
            ctrl.checkBox.forEach(function(project, index){
                if(!ctrl.showError){
                    if(project){
                        deleteObjects.push(ctrl.data.projects[index].name)
                    }
                }
              });
            confirmModal("Delete", 'projects', ctrl.batchDelete, deleteObjects);
        }

        /**
         * This will open the modal that will show the delete confirm
         * message
         */
        function openDeleteModal(name) {
            confirmModal("Delete",'projects', ctrl.projectDelete, name);
        }

        ctrl.listProjects();
    }

    /**
     * TestAPI Project  Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the project's details
     */
    angular.module('testapiApp').controller('ProjectModalCtrl', ProjectModalCtrl);
    ProjectModalCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function ProjectModalCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.createRequirements = [
            {label: 'name', type: 'text', required: true},
            {label: 'description', type: 'textarea', required: false}
        ];
        ctrl.project = {
            name : '',
            description : ''
        }
        if(ctrl.data.project){
            ctrl.projectName = ctrl.data.project.name
            ctrl.project = ctrl.data.project
            delete ctrl.project._id;
        }

        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            if (angular.isDefined(ctrl.data.successHandler)) {
                if(ctrl.project.name != ""){
                    var success = false;
                    if(ctrl.data.project){
                       ctrl.data.successHandler(ctrl.projectName, ctrl.project).success(function (data){
                            $uibModalInstance.close();
                       })
                    }else{
                        ctrl.data.successHandler(ctrl.project).success(function (data){
                            $uibModalInstance.close();
                        })
                    }
                }else{
                    ctrl.showCreateError = true;
                    ctrl.error = 'Name is missing.'
                }
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
