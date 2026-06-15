from flask import Flask

from mediawiki_monitor.routes import create_wikistat_blueprint


def main() -> None:
    """Entry point."""
    app = Flask(__name__)

    wikistat_blueprint = create_wikistat_blueprint()

    app.register_blueprint(wikistat_blueprint)

    app.run()


if __name__ == "__main__":
    main()
