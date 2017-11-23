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
            ctrl.showCreateError = false;
            ctrl.showCreateSuccess = false;
            if(ctrl.name != ""){
                var projects_url = ctrl.url;
                var body = {
                    name: ctrl.name,
                    description: ctrl.description
                };
                ctrl.projectsRequest =
                    $http.post(projects_url, body).success(function (data){
                        ctrl.showCreateSuccess = true ;
                        ctrl.update();
                    }).catch(function (data) {
                        ctrl.showCreateError = true;
                        ctrl.error = data.statusText;
                    });
                ctrl.name = "";
                ctrl.description="";
            }
            else{
                ctrl.showCreateError = true;
                ctrl.error = 'Name is missing.'
            }
        }

        /**
         * This will contact the TestAPI to get a listing of declared projects.
         */
        function update() {
            ctrl.showUpdateError = false;
            var content_url = ctrl.url + '?';
            var name  = ctrl.filterName;
            if(name){
                content_url = content_url + 'name=' +
                name;
            }
            ctrl.resultsRequest =
                $http.get(content_url).success(function (data) {
                    ctrl.data = data;
                }).catch(function (data)  {
                    ctrl.data = null;
                    ctrl.showUpdateError = true;
                    ctrl.error = data.statusText;
                });
        }

        /**
         * This function will clear all filters and update the projects
         * listing.
         */
        function clearFilters() {
            ctrl.filterName = null;
            ctrl.showUpdateError = false;
            ctrl.update();
        }
    }
})();
