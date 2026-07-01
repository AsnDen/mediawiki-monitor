from collections.abc import KeysView

from flask import Blueprint, render_template, request
from httpx import TimeoutException

from mediawiki_monitor.config import URLS
from mediawiki_monitor.service import MediawikiAPIService


def _get_wikifamily_links() -> KeysView[str]:
    return URLS.keys()


def create_wikistat_blueprint() -> Blueprint:
    bp = Blueprint("wikistat", __name__)

    @bp.context_processor
    def inject_links() -> dict[str, KeysView[str]]:  # pyright: ignore[reportUnusedFunction]
        return {"families": _get_wikifamily_links()}

    @bp.get("/wikistat/")
    def wikistat() -> str:  # pyright: ignore[reportUnusedFunction]
        return render_template(
            "wikistat/wikistat/wikistat.html",
        )

    @bp.get("/wikistat/<string:family>")
    def family(family: str) -> str:  # pyright: ignore[reportUnusedFunction]
        url = URLS.get(family)

        if not url:
            return render_template(
                "wikistat/error.html",
                message="Некорректная ссылка на вики-проект.",
            )

        try:
            with MediawikiAPIService(url) as service:
                site_info = service.get_site_info()
                statistics = service.get_statistics()
                recent_changes = service.get_recent_changes(10)
        except TimeoutException:
            return render_template(
                "wikistat/error.html",
                message="Вики-проект на данный момент недоступен. Попробуйте позже.",
            )

        arcitcle_path = site_info["server"] + site_info["articlepath"].replace("$1", "")
        script = site_info["server"] + site_info["script"]

        return render_template(
            "wikistat/wikifamily/wikifamily.html",
            base=site_info["base"],
            sitename=site_info["sitename"],
            logo=site_info["logo"],
            generator=site_info["generator"],
            phpversion=site_info["phpversion"],
            pages=statistics["pages"],
            articles=statistics["articles"],
            edits=statistics["edits"],
            images=statistics["images"],
            users=statistics["users"],
            activeusers=statistics["activeusers"],
            admins=statistics["admins"],
            jobs=statistics["jobs"],
            family=family,
            article_path=arcitcle_path,
            script=script,
            recent_changes=recent_changes,
        )

    @bp.get("/wikistat/<string:family>/diff")
    def diff_view(family: str) -> str:  # pyright: ignore[reportUnusedFunction]
        url = URLS.get(family)

        if not url:
            return render_template(
                "wikistat/error.html",
                message="Некорректная ссылка на вики-проект.",
            )

        title = request.args.get("title")
        diff = request.args.get("diff", type=int)
        old_diff = request.args.get("old_diff", type=int)

        if not (diff and old_diff):
            return render_template(
                "wikistat/error.html",
                message="Невозможно создать diff для страницы.",
            )

        try:
            with MediawikiAPIService(url) as service:
                diff_view = service.get_diff(old_diff, diff)
        except TimeoutException:
            return render_template(
                "wikistat/error.html",
                message="Вики-проект на данный момент недоступен. Попробуйте позже.",
            )

        return render_template(
            "wikistat/diff.html",
            wiki_page_title=title,
            diff=diff_view,
            family=family,
        )

    return bp
