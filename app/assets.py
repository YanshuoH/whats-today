from flask_assets import Bundle

css = Bundle(
    'built/bootstrap.css',
    Bundle(
        'sass/main.scss',
        filters='pyscss'
    ),
    filters='cssmin', output='built/common.css')

js = Bundle(
    'components/jquery/dist/jquery.min.js',
    'components/bootstrap/dist/js/bootstrap.min.js',
    # Bundle(
    #     'js/main.js',
    #     filters='closure_js'
    # ),
    )