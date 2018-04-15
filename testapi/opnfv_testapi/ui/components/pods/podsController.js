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
        .controller('PodsController', PodsController);

    PodsController.$inject = [
        '$scope', '$http', '$filter', '$state', '$window', '$uibModal', 'testapiApiUrl','raiseAlert',
        'confirmModal', 'keepState', 'sortService', '$timeout'
    ];

    /**
     * TestAPI Pods Controller
     * This controller is for the '/pods' page where a user can browse
     * through pods declared in TestAPI.
     */
    function PodsController($scope, $http, $filter, $state, $window, $uibModal, testapiApiUrl,
        raiseAlert, confirmModal, keepState, sortService, $timeout) {
        var ctrl = this;
        ctrl.url = testapiApiUrl + '/pods';
        ctrl.checkBox = []
        ctrl.checkBoxList = [];
        ctrl.sorting = {};

        ctrl.create = create;
        ctrl.listPods = listPods;
        ctrl.open = open;
        ctrl.filter = 'name'
        ctrl.openDeleteModal = openDeleteModal
        ctrl.openBatchDeleteModal = openBatchDeleteModal
        ctrl.openCreateModal = openCreateModal
        ctrl.podDelete = podDelete
        ctrl.batchDelete = batchDelete;
        ctrl.viewPod = viewPod
        ctrl.sortBy = sortBy
        ctrl.toastError = toastError
        ctrl.toastSuccess = toastSuccess

        function toastError() {
            ctrl.showError = true
            $timeout(function(){ ctrl.showError = false;}, 3000);
        }

        function toastSuccess() {
            ctrl.showSuccess = true
            $timeout(function(){ ctrl.showSuccess = false;}, 3000);
        }

        function sortBy(field){
            ctrl.data.pods = sortService.sortFunction(ctrl.data.pods, field , ctrl.sorting[field] )
            ctrl.sorting[field]=!ctrl.sorting[field]
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


        /**
         * This will contact the TestAPI to create a new pod.
         */
        function create(pod) {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            if(pod.name != ""){
                var pods_url = ctrl.url;
                var body = {
                    name: pod.name,
                    mode: pod.mode,
                    role: pod.role,
                    details: pod.details
                };
                ctrl.podsRequest =
                    $http.post(pods_url, body).success(function (data) {
                        ctrl.success = "Create Success"
                        ctrl.toastSuccess()
                        ctrl.listPods();
                    }).catch(function (data)  {
                        ctrl.error = data.statusText;
                        ctrl.toastError()
                    });
            }
            else{
                ctrl.error = 'Name is missing.'
                ctrl.toastError()
            }
        }

        /**
         * This will contact the TestAPI to get a listing of declared pods.
         */
        function listPods() {
            ctrl.showError = false;
            var reqURL = ctrl.url;
            if(ctrl.filterText!=undefined){
                reqURL = ctrl.url + "?name=" + ctrl.filterText
            }
            else if(keepState.filter.podFilter){
                for (var filter in keepState.filter.podFilter){
                    reqURL = ctrl.url + '?' + filter + '=' + keepState.filter.podFilter[filter]
                    ctrl.filterText = keepState.filter.podFilter[filter]
                }
            }
            ctrl.podsRequest =
                $http.get(reqURL).success(function (data) {
                    ctrl.data = data;
                    ctrl.sortBy("name")
                    if(ctrl.filterText != undefined){
                        keepState.filter.podFilter = {
                            'name': ctrl.filterText
                        }
                    }
                }).catch(function (data) {
                    ctrl.data = null;
                    ctrl.error = data.statusText;
                    ctrl.toastError()
                });
        }

        function viewPod(name){
            $state.go('pod', {'name':name}, {reload: true});
        }
        /**
         * This will contact the TestAPI to delete a pod for given
         * name.
         */
        function podDelete(podName){
            var pods_url = ctrl.url + "/" + podName
            $http.delete(pods_url).success(function(){
                ctrl.success = "Delete Success"
                ctrl.toastSuccess()
                ctrl.listPods();
            }).catch(function (data)  {
                ctrl.error = data.statusText;
                ctrl.toastError()
            });
        }

        /**
         * This will  delete list of pods.
         */
        function batchDelete(){
            var index;
            var checkedBox = [];
            for(index in ctrl.checkBox){
                if(!ctrl.showError){
                    if(ctrl.checkBox[index]){
                        podDelete(ctrl.data.pods[index].name);
                    }
                }
            }
            ctrl.checkBox = []
        }

        /**
         * This will open the modal that will show the batch delete confirm
         * message
         */
        function openBatchDeleteModal() {
            var deleteObjects = []
            for(var index in ctrl.checkBox){
                if(ctrl.checkBox[index]){
                    deleteObjects.push(ctrl.data.pods[index].name)
                }
            }
            confirmModal("Delete", 'pods', ctrl.batchDelete, deleteObjects);
        }

        /**
         * This will open the modal that will show the delete confirm
         * message
         */
        function openDeleteModal(name) {
            confirmModal("Delete", 'pod', ctrl.podDelete, name);
        }

        /**
         * This will open the modal that will show the create
         * view
         */
        function openCreateModal(){
            $uibModal.open({
                templateUrl: 'testapi-ui/components/pods/modals/createModal.html',
                controller: 'PodModalCtrl as PodModalCtrl',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: "Create",
                            successHandler: ctrl.create,
                        };
                    }
                }
            });
        }

        ctrl.listPods();
    }


    /**
     * TestAPI Pod Modal Controller
     * This controller is for the create modal where a user can create
     * the project information and for the edit modal where user can
     * edit the pods details
     */
    angular.module('testapiApp').controller('PodModalCtrl', PodModalCtrl);
    PodModalCtrl.$inject = ['$scope', '$uibModalInstance', 'data'];
    function PodModalCtrl($scope, $uibModalInstance, data) {
        var ctrl = this;
        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.data = angular.copy(data);
        ctrl.roles = ['community-ci', 'production-ci'];
        ctrl.modes = ['metal', 'virtual'];
        ctrl.createRequirements = [
            {label: 'name', type: 'text', required: true},
            {label: 'mode', type: 'select', selects: ctrl.modes},
            {label: 'role', type: 'select', selects: ctrl.roles},
            {label: 'details', type: 'textarea', required: false}
        ];
        ctrl.pod = {
            name : '',
            role : 'community-ci',
            mode : 'metal',
            details : ''
        }

        if(ctrl.data.pod){
            ctrl.pod = ctrl.data.pod
        }

        /**
         * Initiate confirmation and call the success handler with the
         * inputs.
         */
        function confirm() {
            $uibModalInstance.close();
            if (angular.isDefined(ctrl.data.successHandler)) {
                ctrl.data.successHandler(ctrl.pod);
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

