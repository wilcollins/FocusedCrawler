module.exports = function(grunt) {

  // Project configuration.
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),

    jshint: {
      options: {
        reporterOutput: "",
        esnext: 6,

         globals: {
          //jQuery: true,
          console: true,
          module: true,
          document: true
        },
        ignores: ["**/node_modules/**", "**/bower_components/**"]
      },
      all: ['Gruntfile.js', '*.js', 'js/**/*.js', 'routes/**/*.js'] // 'public/**/*.js' , 'site/**/*.js'
    },

    // RUN THIS TASK WHENEVR THE HOOKS CHANGE, ie. `grunt githooks`
    githooks: {
      all: {
        'pre-commit': 'jshint casperjs',
      }
    },

    // uglify: {
    //   options: {
    //     banner: '/*! <%= pkg.name %> <%= grunt.template.today("yyyy-mm-dd") %> */\n'
    //   },
    //   build: {
    //     src: 'src/<%= pkg.name %>.js',
    //     dest: 'build/<%= pkg.name %>.min.js'
    //   }
    // },

    // CASPERJS TESTING
    casperjs: {
      options: {
        async: {
          parallel: true
        },
        silent: false
      },
      files: ['test/casperjs/**/*.js']
    },

    // AUTO-TRIGGER JSHINT ON FILE CHANGE
    watch: {
        files: ['Gruntfile.js'],
        tasks: ['jshint']
    }

  });

  //grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-casperjs');
  grunt.loadNpmTasks('grunt-githooks');
  grunt.loadNpmTasks('grunt-contrib-jshint');

  // Default task(s).
  grunt.registerTask('default', ['jshint', 'casperjs']);

  grunt.registerTask('test', ['jshint', 'casperjs']);

};
