import flask


def create_application(debug=False, verbose=False):
    import soonerface.config

    app = flask.Flask(__name__)
    app.debug = debug
    app.config.from_object('soonerface.config')

    from soonerface.views import main
    app.register_blueprint(main)

    return app
