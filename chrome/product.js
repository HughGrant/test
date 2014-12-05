var product = angular.module("Product", ["PortiaServices"])

product.controller('ProductListCtrl', ['$scope', '$filter', 'common', function($scope, $filter, common) {
	// inital setting
  $scope.check = false
	$scope.model_name = 'products'
  // toggling form
  $scope.toggle = function() {
    $('#' + $scope.model_name + "Modal").modal("toggle")
  }
  // first get titles
  $scope.metas = common.meta($scope.model_name).query()

  // list first page data
  var model = common.rest($scope.model_name)
  $scope.model = model
  $scope.temp = new model()

  $scope.query = function(limit, page) {
    model.query({limit: limit, page: page}, function(records) {
      angular.forEach(records, function(object) {
        object.check = false
        object.id = object._id.$oid
      })
      $scope.records = records
    })
  }

  // select all check box
  $scope.check_all = function() {
    $scope.check = !$scope.check
    angular.forEach($scope.records, function(object, index) {
      object.check = $scope.check
    })
  }

  // delete selected
  $scope.delete_checked = function() {
    if ($scope.check) {
      var flag = window.confirm("危险: 您确定要删除全选的数据吗?")
      if (!flag) {
        return false;
      }
    }

    var filtered = $filter("filter")($scope.records, {check:false})

    angular.forEach($scope.records, function(record, index) {
      if (record.check === true) {
        record.$remove()
      }
    })

    $scope.records = filtered;
    if ($scope.check) {
      $scope.check = false
    }
  }

  // edit a row
  $scope.edit = function(record) {
    $scope.temp = record
    $scope.toggle()
  }

  // upload a product
  $scope.upload = product_upload

  // pagination
  $scope.limit = 30
  $scope.current = 0

  $scope.query($scope.limit, $scope.current)

  $scope.$watch('limit', function(limit, old) {
    if (limit != old) {
      $scope.query($scope.limit, $scope.current)
    }
  })

  $scope.$watch('current', function(current, old) {
    if (current != old) {
      $scope.query($scope.limit, $scope.current)
    }
  })

  model.count(function(data) {
    $scope.row = data.row
  })

}])