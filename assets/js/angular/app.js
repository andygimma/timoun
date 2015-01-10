
var app = angular.module('myApp', ["ngRoute"]);



app.config(function($routeProvider, $locationProvider) {
      $routeProvider

          // route for the home page
          .when('/', {
              templateUrl: 'assets/js/angular/partials/index.html',
              controller  : 'indexController'
          })
          .when('/about', {
            templateUrl: 'assets/js/angular/partials/about.html',
            controller  : 'aboutController'
          })
          .when('/search', {
            templateUrl: 'assets/js/angular/partials/search.html',
            controller  : 'searchController'
          })          
          .when('/contact', {
            templateUrl: 'assets/js/angular/partials/contact.html',
            controller  : 'contactController'
          }) 
          .when('/suggest_services', {
            templateUrl: 'assets/js/angular/partials/suggest_services.html',
            controller  : 'suggestServicesController'
          }) 
          .when('/mental_illness_services', {
            templateUrl: 'assets/js/angular/partials/mental_illness_services.html',
            controller  : 'mentalIllnessServicesController'
          }) 
//           .when('/*', {
//               templateUrl: 'assets/js/angular/partials/index.html',
//               controller  : 'indexController'
//           })
          
          .otherwise({
              redirectTo: '/'
            });
          $locationProvider.html5Mode(true);

    });
app.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('{[').endSymbol(']}');
});
app.controller('indexController', function($scope) {

});

app.controller('aboutController', function($scope) {

});

app.controller('searchController', function($scope) {

});
    
app.controller('contactController', function($scope) {

});

app.controller('suggestServicesController', function($scope) {

});

app.controller('mentalIllnessServicesController', function($scope) {

});