// var text = '{"employees":[' +
// '{"firstName":"John","lastName":"Doe" },' +
// '{"firstName":"Anna","lastName":"Smith" },' +
// '{"firstName":"Peter","lastName":"Jones" }]}';

// obj = JSON.parse(text);
// document.getElementById("demo").innerHTML =
// obj.employees[1].firstName + " " + obj.employees[1].lastName;
var app = angular.module('myApp', []);
app.controller('formCtrl', function($scope) {
    
    $scope.master = {fName:"", lName:"", city:"", state:"", zip:"", agree: ""};
    $scope.user = angular.copy($scope.master);

});