'use strict';
var gulp = require("gulp");
var webpack = require("webpack-stream");

gulp.task("webpack", function() {
    return gulp.src(['./src/app.tsx']).pipe(webpack({
			output: {
				filename: 'app.js'
			},
			resolve: {
				extensions: ['', '.webpack.js', '.web.js', '.tsx', '.ts', '.js']
			},
			module: {
				loaders: [{test: /\.(ts|tsx)$/, loader: 'ts-loader'}]
			}
		})).pipe(gulp.dest('./dist/'));
});

gulp.task("build", ["webpack"]);