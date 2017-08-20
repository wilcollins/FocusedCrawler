var ph = require('public-hostname');
var fs = require('fs');
var source = require('shell-source');

var Utils = {
  // returns { }
  getPublicHostname: function(cb){
    ph(function(err, data){
      cb(data);
    });
  },

  getIP: function(cb){
    Utils.getPublicHostname(function(data){
      cb(data.address);
    });
  },

  getHostname: function(cb){
    Utils.getPublicHostname(function(data){
      cb(data.hostname);
    });
  },

  getEnv: function(cb, will_log=false){
      Utils.getPublicHostname(function(data){
        var hostname = data.hostname;
        var ip = data.address;

        var isProd =  hostname.indexOf("wilcollins.com") > -1 ||
                      hostname.indexOf("amazonaws.com") > -1;
        var isLocalhost = !isProd;

        var env;
        if(isProd){
          env = "prod";
        }else{
          env = "localhost";
        }

        if(will_log){
          Utils.log("ip : " + ip);
          Utils.log("hostname : " + hostname);
          Utils.log("env : " + env);
        }

         cb(env);
      });
  },

  initEnv: function(cb){

    source(__dirname + '/../../scripts/conf', function(err) {
      if (err) return console.error(err);
      console.log(process.env.LOCAL_PORT);

      // set NODE_ENV by hostname
      Utils.getEnv(function(env){
        process.env.NODE_ENV = env;
        cb(process.env);
      }, true);
    });
  },


  log : function(entry) {
    console.log(entry);
    fs.appendFileSync('/tmp/sample-app.log', new Date().toISOString() + ' - ' + entry + '\n');
  }

};

module.exports = Utils;
