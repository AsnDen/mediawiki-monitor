from flask import Blueprint, render_template, request

from mediawiki_monitor.config import URLS
from mediawiki_monitor.service import MediawikiAPIService


def create_wikistat_blueprint() -> Blueprint:
    bp = Blueprint("wikistat", __name__)

    @bp.get("/wikistat/")
    def wikistat() -> str:  # pyright: ignore[reportUnusedFunction]
        return render_template(
            "wikistat/wikistat/wikistat.html",
            families=URLS.keys(),
        )

    @bp.get("/wikistat/<string:family>")
    def family(family: str) -> str:  # pyright: ignore[reportUnusedFunction]
        url = URLS.get(family)

        # TODO (asnden): return error page
        if not url:
            return render_template("base.html")

        with MediawikiAPIService(url) as service:
            site_info = service.get_site_info()
            statistics = service.get_statistics()
            recent_changes = service.get_recent_changes(10)

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
            recent_changes=recent_changes,
        )

    @bp.get("/wikistat/<string:family>/diff")
    def diff_view(family: str) -> str:  # pyright: ignore[reportUnusedFunction]
        url = URLS[family]

        # TODO (asnden): return error page
        if not url:
            return render_template("base.html")

        title = request.args.get("title")
        diff = request.args.get("diff", type=int)
        old_diff = request.args.get("old_diff", type=int)

        # TODO (asnden): return error page
        if not (diff and old_diff):
            return render_template("base.html")

        with MediawikiAPIService(url) as service:
            diff_view = service.get_diff(old_diff, diff)

        return render_template(
            "wikistat/diff.html",
            wiki_page_title=title,
            diff=diff_view,
        )

    return bp
