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
                recent_changes = service.get_recent_changes(100)
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

        to_rev = request.args.get("to_rev", type=int)
        from_rev = request.args.get("from_rev", type=int)

        to_id = request.args.get("to_id", type=int)
        from_id = request.args.get("from_id", type=int)

        try:
            with MediawikiAPIService(url) as service:
                if to_id and from_id:
                    diff_view = service.get_diff_by_page_ids(from_id, to_id)
                elif to_rev and from_rev:
                    diff_view = service.get_diff(from_rev, to_rev)
                else:
                    return render_template(
                        "wikistat/error.html",
                        message="Невозможно создать diff. Недостаточно параметров.",
                    )
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

    @bp.get("/wikistat/<string:family>/<string:user>")
    def user(family: str, user: str) -> str:  # pyright: ignore[reportUnusedFunction]
        url = URLS.get(family)

        if not url:
            return render_template(
                "wikistat/error.html",
                message="Некорректная ссылка на вики-проект.",
            )

        try:
            with MediawikiAPIService(url) as service:
                user_contribs = service.get_user_contributions(user, 100)
                # TODO (asnden): remove side_info
                # and think about better way to get `script`
                site_info = service.get_site_info()
        except TimeoutException:
            return render_template(
                "wikistat/error.html",
                message="Вики-проект на данный момент недоступен. Попробуйте позже.",
            )

        script = site_info["server"] + site_info["script"]

        return render_template(
            "wikistat/user/user.html",
            user_contribs=user_contribs,
            script=script,
            family=family,
            user=user,
        )

    return bp
