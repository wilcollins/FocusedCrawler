var express = require('express');
var router = express.Router();
var PythonShell = require('python-shell');

/* GET home page. */
router.get('/crawl', function(req, res, next) {

  var options = {
    mode: 'text',
    pythonOptions: [],
    scriptPath: __dirname + '/../../crawler/',
    args: [
      "--seeds",
      "trump",

      "--blacklist_domains",
      "www.breitbart.com",

      "--relevancy_threshold",
      "0.8",

      "--irrelevancy_threshold",
      "0.7",

      "--page_limit",
      "1",

      "--link_limit",
      "1",

      "--adaptive",
      "true",

      "--relevant_urls",
      "www.cnn.com",

      "--irrelevant_urls",
      "www.foxnews.com"
    ]
  };

  PythonShell.run('FocusedCrawler.py', options, function (err, results) {
    if (err) throw err;
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
    res.send(results);
  });

});

module.exports = router;
