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
        '$scope', '$http', '$filter', '$state', 'testapiApiUrl','raiseAlert'
    ];

    /**
     * TestAPI Project Controller
     * This controller is for the '/projects' page where a user can browse
     * through projects declared in TestAPI.
     */
    function ProjectsController($scope, $http, $filter, $state, testapiApiUrl,
        raiseAlert) {
        var ctrl = this;
        ctrl.url = testapiApiUrl + '/projects';
        ctrl.create = create;
        ctrl.update = update;
        ctrl.open = open;
        ctrl.clearFilters = clearFilters;

        ctrl.createRequirements = [
            {label: 'name', type: 'text', required: true},
            {label: 'description', type: 'textarea', required: false}
        ];

        ctrl.name = '';
        ctrl.details = '';
        ctrl.filterName='';
        /**
         * This will contact the TestAPI to create a new project.
         */
        function create() {
            ctrl.showError = false;
            ctrl.showSuccess = false;
            if(ctrl.name != ""){
                var projects_url = ctrl.url;
                var body = {
                    name: ctrl.name,
                    description: ctrl.description
                };
                ctrl.projectsRequest =
                    $http.post(projects_url, body).success(function (data){
                        ctrl.showSuccess = true ;
                        ctrl.update();
                    }).catch(function (data) {
                        ctrl.showError = true;
                        ctrl.error = 'Error creating the new Project from server:' + data.statusText;
                    });
                ctrl.name = "";
                ctrl.description="";
            }
            else{
                ctrl.showError = true;
                ctrl.error = 'Name is missing.'
            }
        }

        /**
         * This will contact the TestAPI to get a listing of declared projects.
         */
        function update() {
            ctrl.showError = false;
            var content_url = ctrl.url + '?';
            var start = $filter('date')(ctrl.startDate, 'yyyy-MM-dd');
            var name  = ctrl.filterName;
            if(name){
                content_url = content_url + 'name=' +
                name + '&';
            }
            if (start) {
                content_url = content_url + 'start=' +
                start + "&";
            }
            var end = $filter('date')(ctrl.endDate, 'yyyy-MM-dd');
            if (end) {
                content_url = content_url + 'end=' +
                end;
            }
            ctrl.resultsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.data = data;
                }).catch(function (data)  {
                    ctrl.data = null;
                    ctrl.showError = true;
                    ctrl.error = "Error retrieving results listing from server: " + data.statusText;
                });
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
         * This function will clear all filters and update the results
         * listing.
         */
        function clearFilters() {
            ctrl.startDate = null;
            ctrl.endDate = null;
            ctrl.update();
        }
    }
})();
