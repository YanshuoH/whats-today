var gulp = require('gulp');
var sass = require('gulp-sass');

var styles = 'integ/styles/*.scss';
var dest = 'integ/built';

gulp.task('sass', function () {
  return gulp.src(styles)
    .pipe(sass())
    .pipe(gulp.dest(dest));
});

gulp.task('watch', function () {
  gulp.watch(styles, ['sass']);
});

gulp.task('default', ['watch', 'sass']);
