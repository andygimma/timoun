
var app = angular.module('myApp', ["ui.router"]).config(function($stateProvider, $urlRouterProvider, $locationProvider) {
  $locationProvider.html5Mode(true);

  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/");
  //
  // Now set up the states
  $stateProvider

    .state('index', {
      url: "/",
      templateUrl: "assets/js/angular/partials/index.html",
    })
    .state('about', {
      url: "/about",
      templateUrl: "assets/js/angular/partials/about.html",
    })
    .state('search', {
      url: "/search",
      templateUrl: "assets/js/angular/partials/search.html",
    })
    .state('contact', {
      url: "/contact",
      templateUrl: "assets/js/angular/partials/contact.html",
    })
    .state('suggest_services', {
      url: "/suggest_services",
      templateUrl: "assets/js/angular/partials/suggest_services.html",
    })
    .state('mental_illness_services', {
      url: "/mental_illness_services",
      templateUrl: "assets/js/angular/partials/mental_illness_services.html",
    })
    .state('login', {
      url: "/users/login",
      templateUrl: "../assets/js/angular/partials/login.html",
    })
    .state('reset_password', {
      url: "/users/reset_password",
      templateUrl: "../assets/js/angular/partials/reset_password.html",
    })
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

app.controller('adminIndexController', function($scope) {

});
