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

list_page_react_js = Bundle(
    'components/react/react.min.js',
    'js/list_react_ctrl.js')

today_page_react_js = Bundle(
    'components/marked/marked.min.js',
    'components/react/react.min.js',
    'js/today_react_ctrl.js')

form_page_js = Bundle(
    'components/marked/marked.min.js')