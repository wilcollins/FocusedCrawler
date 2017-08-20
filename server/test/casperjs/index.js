var SERVER = "http://localhost";

var tests = [
  {
    "url": SERVER,

    "verify" : function(test){
      return function(){
        var res = this.status(false);
        test.assert(res.currentHTTPStatus === 200, "page returns a 200 status code");
        test.assertTitle("Express", "Title check");
      }
    },

    "numVerifications": 2
  }
];

var numVerifications = 0;
for(var i = 0; i < tests.length; i++){
  var test = tests[i];
  var numAssertions = test["numVerifications"];
  numVerifications += numAssertions;
}
casper.test.begin('API Test', numVerifications, function (test) {

  for(var i = 0; i < tests.length; i++){
    var test_data = tests[i];
    var endpoint = test_data["url"];
    var test_func = test_data["verify"];
    casper.start(endpoint, test_func(test));
  }

  casper.run(function() {
    test.done();
  });

});
