from flask import Flask

from mediawiki_monitor.routes import create_wikistat_blueprint


def create_app() -> Flask:
    """App factory."""
    app = Flask(__name__)

    app.register_blueprint(create_wikistat_blueprint())

    return app


def run_app() -> None:
    """Runs app locally for tests."""
    app = create_app()
    app.run(host="127.0.0.1", port=8000)


if __name__ == "__main__":
    run_app()
