// datepicker configuration for target date
$(document).ready(function(){
    $( "#dt" ).datepicker({dateFormat: 'yy-mm-dd', minDate: 0 });
})
            
// knockout validation configuration
ko.validation.init({
    registerExtenders: true,
    messagesOnModified: true,
    insertMessages: true,
    parseInputAttributes: true,
    messageTemplate: null
}, true);

// initialize feature request view model
function FeatureReqViewModel() {
  var self = this; 
  self.validateNow = ko.observable(false);
  self.client_list = ko.observableArray();
  self.product_area_list = ko.observableArray();
  self.req_title = ko.observable().extend({ required: true });
  self.req_desc = ko.observable();
  self.req_target_date = ko.observable().extend({
      required: { message: 'Target Date Is Mandatory' },
  }); 
  self.req_client_priority = ko.observable().extend({ 
      min: 1, 
      required: { message: 'Priority Should Be Greater Than 0'}
  });
  self.req_pro_area = ko.observable();
  self.req_client = ko.observable();          
  self.feature_requests_array = ko.observableArray();
  self.errors = ko.validation.group(self);

  // get all feature requests, clients & product area list
  self.getAllRequests = function() {          
    $.getJSON("/feature_request_list/", function(allData) {
      self.feature_requests_array(allData.feature_requests);
      self.client_list(allData.clients)
      self.product_area_list(allData.product_areas)
    });
  }


  // create new feature request
  self.form_post = function() {
        self.validateNow = ko.observable(true);
        if (self.errors().length == 0) {
            var data = {
              'client': self.req_client().id,
              'product_area': self.req_pro_area().id,
              'client_priority': self.req_client_priority(),
              'target_date': self.req_target_date(),
              'title': self.req_title(),
              'description': self.req_desc()
            };
            $.ajax("/feature_request_list/", {
                data: data,
                type: "POST",                     
                success: function(result) {
                  self.feature_requests_array.removeAll();
                  self.getAllRequests();                       
                  alert(result)
                  $("#myModal .close").click()                       
                },
                error: function(result){ 
                  alert(result.responseText);
                }               
            });

        } else {
            self.errors.showAllMessages();
        }       
      };
  self.getAllRequests();
};

//Custom Binding for target date formate
ko.bindingHandlers.formatDate = {
    update: function (element, valueAccessor, allBindingsAccessor, 
            viewModel, bindingContext) {
        var value = valueAccessor();
        var newValueAccessor = ko.unwrap(value);
        var dt = new Date(newValueAccessor);
        if (newValueAccessor !== null) $(element).text(
                    dt.toLocaleDateString());
    }
};

ko.applyBindings(new FeatureReqViewModel());                   
