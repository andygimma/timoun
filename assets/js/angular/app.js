  var app = angular.module('myApp', ["ngRoute"]);

      app.config(function($interpolateProvider){
          $interpolateProvider.startSymbol('{[').endSymbol(']}');
      });
      
      app.config(function($routeProvider) {
            $routeProvider

                // route for the home page
                .when('/', {
                    templateUrl: 'assets/js/angular/partials/add_order.html',
                    controller  : 'mainController'
                })
                .when('/second', {
                    templateUrl: 'assets/js/angular/partials/about.html',
                    controller  : 'aboutController'
                })

                // route for the about page
                .otherwise({
                    redirectTo: '/'
                  });
        });
        
        app.controller('mainController', function($scope) {
        // create a message to display in our view
        $scope.message = 'Look! I am an about page.';

        console.log($scope.message);
    });

    app.controller('aboutController', function($scope) {
        $scope.message = 'Look! I am an about page.';
    });

    app.controller('contactController', function($scope) {
        $scope.message = 'Contact us! JK. This is just a demo.';
    });
    