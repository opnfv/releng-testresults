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
        .controller('DeployResultsController', DeployResultsController);

    DeployResultsController.$inject = [
        '$scope', '$http', '$filter', '$state', 'testapiApiUrl','raiseAlert'
    ];

    /**
     * TestAPI Deploy Results Controller
     * This controller is for the '/deployresults' page where a user can browse
     * a listing of community uploaded results.
     */
    function DeployResultsController($scope, $http, $filter, $state, testapiApiUrl,
        raiseAlert) {
        var ctrl = this;

        ctrl.open = open;
        ctrl.clearFilters = clearFilters;
        ctrl.deleteTag = deleteTag;
        ctrl.filterList= filterList;
        ctrl.testFilter = testFilter
        ctrl.filter = "pod"
        ctrl.filterValue = "pod_name"
        ctrl.encodeFilter = encodeFilter
        ctrl.viewDeployResult = viewDeployResult
        ctrl.tagArray = {}
        ctrl.filterOption=[]

        /** Initial page to be on. */
        ctrl.currentPage = 1;

        /**
         * How many results should display on each page. Since pagination
         * is server-side implemented, this value should match the
         * 'results_per_page' configuration of the TestAPI server which
         * defaults to 20.
         */
        ctrl.itemsPerPage = 20;

        /**
         * How many page buttons should be displayed at max before adding
         * the '...' button.
         */
        ctrl.maxSize = 5;

        /** The upload date lower limit to be used in filtering results. */
        ctrl.startDate = '';

        /** The upload date upper limit to be used in filtering results. */
        ctrl.endDate = '';

        /** The date format for the date picker. */
        ctrl.format = 'yyyy-MM-dd';

        ctrl.pageHeader = "Deploy Results"

        ctrl.pageParagraph = 'Your most recently uploaded deploy results are listed here.'
        ctrl.isPublic = false;

        function encodeFilter(){
            ctrl.filterText = ''
            ctrl.filterOption=[]
            if(ctrl.filter=="pod" || ctrl.filter=="scenario"){
                var reqURL = testapiApiUrl +"/" + ctrl.filter + "s"
                ctrl.datasRequest =
                    $http.get(reqURL).success(function (data) {
                        ctrl.filterData = data;
                        for(var index in ctrl.filterData[ctrl.filter + "s"]){
                            if( ctrl.filterOption.indexOf(ctrl.filterData[ctrl.filter + "s"][index]["name"]) < 0){
                                ctrl.filterOption.push(ctrl.filterData[ctrl.filter + "s"][index]["name"])
                            }
                        }
                    }).catch(function (data) {
                        ctrl.data = null;
                        ctrl.showError = true;
                        ctrl.error = data.statusText;
                    });

            }
        }

        function deleteTag(index){
            delete  ctrl.tagArray[index];
            ctrl.filterList();
        }

        function testFilter(text){
            for (var filter in ctrl.tagArray){
                if(text==filter){
                    return true;
                }
            }
            return false;
        }

        function viewDeployResult(_id){
            $state.go('deployresult', {'_id':_id}, {reload: true});
        }

        /**
         * This will contact the TestAPI API to get a listing of deploy
         * results.
         */
        function filterList(){
            if(ctrl.filter && ctrl.filterText!="" && ctrl.filterText!=undefined){
                ctrl.tagArray[ctrl.filter] =  ctrl.filterText;
            }
            ctrl.showError = false;
            var content_url = testapiApiUrl + '/deployresults' +
                '?page=' + ctrl.currentPage;
            for(var key in ctrl.tagArray){
                if(key=="start_date"){
                    var start = $filter('date')(ctrl.tagArray[key], 'yyyy-MM-dd');
                    if (start) {
                        content_url =
                            content_url + '&from=' + start + ' 00:00:00';
                    }
                }
                else if(key=="end_date"){
                    var end = $filter('date')(ctrl.tagArray[key], 'yyyy-MM-dd');
                    if (end) {
                        content_url = content_url + '&to=' + end + ' 23:59:59';
                    }
                }
                else{
                    content_url = content_url + "&" + key + "=" + ctrl.tagArray[key]
                }
                if (ctrl.isUserResults) {
                    content_url = content_url + '&signed';
                }
            }
            ctrl.resultsRequest =
                    $http.get(content_url).success(function (data) {
                        ctrl.data = data;
                        ctrl.totalItems = ctrl.data.pagination.total_pages * ctrl.itemsPerPage;
                        ctrl.currentPage = ctrl.data.pagination.current_page;
                        ctrl.encodeFilter();
                    }).catch(function (error) {
                        ctrl.data = null;
                        ctrl.totalItems = 0;
                        ctrl.showError = true;
                        ctrl.error = error.statusText
                    });
            ctrl.filterText = ''
        }
        ctrl.filterList();


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
            ctrl.tagArray = {}
            ctrl.filter = undefined
            ctrl.filterList();
        }
    }
})();
