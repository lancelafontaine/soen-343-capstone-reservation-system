(function(){

  var gulp = require('gulp');
  var runSequence = require('run-sequence');
  var browserify = require('browserify');
  var source = require('vinyl-source-stream');
  var watch = require('gulp-watch');
  var plumber = require('gulp-plumber');
  var connect = require('gulp-connect');
  var htmlmin = require('gulp-htmlmin');
  var cleanCSS = require('gulp-clean-css');
  var del = require('del');
  var concat = require('gulp-concat');
  var uglify = require('gulp-uglify');

  gulp.task('default', ['build']);

  gulp.task('build', function() {
    runSequence('clean', 'html', 'css', 'js', 'uglifyjs', 'watch');
  });

  gulp.task('clean', function() {
    return del([
      'build/*',
    ]);
  });

  gulp.task('html', function() {
    return gulp.src('html/*.html')
      .pipe(htmlmin({collapseWhitespace: true}))
      .pipe(gulp.dest('build'));
  });

  gulp.task('css', function() {
    return gulp.src(['css/*.css', 'css/library/*.css', 'node_modules/fullcalendar/dist/fullcalendar.css'])
      .pipe(cleanCSS({compatibility: 'ie8'}))
      .pipe(concat('style.css'))
      .pipe(gulp.dest('build'));
  });

  gulp.task('js', function() {
    return browserify('js/imports.js')
      .bundle()
      .pipe(source('bundle.js'))
      .pipe(gulp.dest('build'));
  });

  gulp.task('uglifyjs', function() {
    return gulp.src('build/*.js')
      .pipe(uglify())
      .pipe(gulp.dest('build'));
  });

  gulp.task('watch', function() {
    watch('js/*.js', function() {
      runSequence('js', 'uglifyjs');
    });
    watch('html/*.html', function() {
      runSequence('html');
    });
    watch('css/*.css', function() {
      runSequence('css');
    });
    connect.server({
      livereload: true,
      directoryListing: true,
      root: ['build']
    });
  });

})();
