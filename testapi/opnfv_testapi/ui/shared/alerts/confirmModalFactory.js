(function () {
    'use strict';

    angular
        .module('testapiApp')
        .factory('confirmModal', confirmModal);

    confirmModal.$inject = ['$uibModal'];

    /**
     * Opens confirm modal dialog with input textbox
     */
    function confirmModal($uibModal) {
        return function(text, resource, successHandler, name) {
            $uibModal.open({
                templateUrl: 'testapi-ui/shared/alerts/confirmModal.html',
                controller: 'CustomConfirmModalController as confirmModal',
                size: 'md',
                resolve: {
                    data: function () {
                        return {
                            text: text,
                            resource: resource,
                            successHandler: successHandler,
                            name: name

                        };
                    }
                }
            });
        };
    }

    angular
        .module('testapiApp')
        .controller('CustomConfirmModalController',
                    CustomConfirmModalController);

    CustomConfirmModalController.$inject = ['$uibModalInstance', 'data'];

    /**
     * This is the controller for the alert pop-up.
     */
    function CustomConfirmModalController($uibModalInstance, data) {
        var ctrl = this;

        ctrl.confirm = confirm;
        ctrl.cancel = cancel;
        ctrl.buildDeleteObjects = buildDeleteObjects;
        ctrl.data = angular.copy(data);

        function buildDeleteObjects(){
            ctrl.deleteObjects = '';
            if (typeof ctrl.data.name === 'string') {
                ctrl.deleteObjects = ctrl.data.name
            }
            else if (ctrl.data.name instanceof Array){
                for(var index in ctrl.data.name){
                    if(index==0){
                        ctrl.deleteObjects += ctrl.data.name[index]
                    }
                    else{
                        ctrl.deleteObjects += ", "+ ctrl.data.name[index]
                    }

                }
            }
            else{
                for(var index in ctrl.data.name[ctrl.data.resource]){
                    if(index==0){
                        ctrl.deleteObjects += ctrl.data.name[ctrl.data.resource][index]
                    }
                    else{
                        ctrl.deleteObjects += ", "+ ctrl.data.name[ctrl.data.resource][index]
                    }

                }
            }
        }
        /**
         * Initiate confirmation and call the success handler with the
         * input text.
         */
        function confirm() {
            $uibModalInstance.close();
            if (angular.isDefined(ctrl.data.successHandler)) {
                ctrl.data.successHandler(ctrl.data.name);
            }
        }

        /**
         * Close the confirm modal without initiating changes.
         */
        function cancel() {
            $uibModalInstance.dismiss('cancel');
        }

        ctrl.buildDeleteObjects();
    }
})();
