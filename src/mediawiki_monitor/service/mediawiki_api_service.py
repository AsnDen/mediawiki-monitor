from dataclasses import dataclass
from typing import NotRequired, Self, TypedDict, cast

from httpx import Client

# TODO (asnden): probably move dataclasses and typeddicts to another file


# Recent changes
class RecentChangePayload(TypedDict):
    revid: int
    old_revid: NotRequired[int]
    title: str
    timestamp: str
    user: str
    comment: str
    type: str


class RecentChangeQueryPayload(TypedDict):
    recentchanges: list[RecentChangePayload]


class RecentChangesResponse(TypedDict):
    query: RecentChangeQueryPayload


@dataclass(slots=True, frozen=True)
class RecentChange:
    revid: int
    old_revid: int | None
    title: str
    timestamp: str
    user: str
    type: str


# Diff compare
CompareResponsePayload = TypedDict(
    "CompareResponsePayload",
    {
        "*": str,
    },
)


class CompareResponse(TypedDict):
    compare: CompareResponsePayload


# Siteinfo
# TODO (asnden): mention in docstring comment that is is NOT full response
class SiteinfoPayload(TypedDict):
    base: str
    sitename: str
    logo: str
    generator: str
    phpversion: str
    server: str
    articlepath: str


class SiteinfoGeneralPayload(TypedDict):
    general: SiteinfoPayload


class SiteinfoResponse(TypedDict):
    query: SiteinfoGeneralPayload


# Statistics
class StatisticsPayload(TypedDict):
    pages: int
    articles: int
    edits: int
    images: int
    users: int
    activeusers: int
    admins: int
    jobs: int


class StatisticsStatisticsPayload(TypedDict):
    statistics: StatisticsPayload


class StatisticsResponse(TypedDict):
    query: StatisticsStatisticsPayload


# User groups
class UserPayload(TypedDict):
    userid: int
    name: str
    editcount: int
    registration: str
    groups: list[str]


@dataclass(slots=True, frozen=True)
class User:
    userid: int
    name: str
    editcount: int
    registration: str
    groups: list[str]


class AllusersPayload(TypedDict):
    allusers: list[UserPayload]


class AllusersResponse(TypedDict):
    query: AllusersPayload


# Libraries and extensions
# TODO (anden): stuff for libraries and extensions

# TODO (asnden): have try-except for raise_for_status


class MediawikiAPIService:
    def __init__(self, api_base_url: str, api_relative_url: str = "api.php") -> None:
        self.client: Client = Client(
            base_url=api_base_url,
            timeout=10.0,
            follow_redirects=True,
        )
        self.api_relative_url: str = api_relative_url

    def get_site_info(self) -> SiteinfoPayload:
        response = self.client.get(
            self.api_relative_url,
            params={
                "action": "query",
                "meta": "siteinfo",
                "format": "json",
            },
        )

        _ = response.raise_for_status()

        data = cast("SiteinfoResponse", response.json())

        return data["query"]["general"]

    def get_statistics(self) -> StatisticsPayload:
        response = self.client.get(
            self.api_relative_url,
            params={
                "action": "query",
                "meta": "siteinfo",
                "format": "json",
                "siprop": "statistics",
            },
        )

        _ = response.raise_for_status()

        data = cast("StatisticsResponse", response.json())

        return data["query"]["statistics"]

    def get_users_by_group(self, groups: tuple[str, ...]) -> list[User]:
        response = self.client.get(
            self.api_relative_url,
            params={
                "action": "query",
                "list": "allusers",
                "format": "json",
                "augroup": "|".join(groups),
                "aulimit": 500,
                "auprop": "editcount|groups|registration",
            },
        )

        _ = response.raise_for_status()

        data = cast("AllusersResponse", response.json())

        return [
            User(
                userid=user["userid"],
                name=user["name"],
                editcount=user["editcount"],
                registration=user["registration"],
                groups=user["groups"],
            )
            for user in data["query"]["allusers"]
        ]

    def get_recent_changes(
        self, total: int, *, no_bots: bool = True
    ) -> list[RecentChange]:
        # TODO (asnden): rerequest in case total > limit (see mediawiki api doc)
        response = self.client.get(
            self.api_relative_url,
            params={
                "action": "query",
                "list": "recentchanges",
                "rclimit": total,
                "format": "json",
                "rcprop": ("ids|title|timestamp|user|comment"),
                "rcnamespace": "*",
                "rcshow": f"{'!' if no_bots else ''}bot",
                "rctype": "new|edit",
            },
        )

        _ = response.raise_for_status()

        data = cast("RecentChangesResponse", response.json())

        return [
            RecentChange(
                revid=rc["revid"],
                old_revid=rc.get("old_revid"),
                title=rc["title"],
                timestamp=rc["timestamp"],
                user=rc["user"],
                type=rc["type"],
            )
            for rc in data["query"]["recentchanges"]
        ]

    def get_diff(self, from_rev: int, to_rev: int) -> str:
        response = self.client.get(
            self.api_relative_url,
            params={
                "action": "compare",
                "fromrev": from_rev,
                "torev": to_rev,
                "prop": "diff",
                "format": "json",
            },
        )

        _ = response.raise_for_status()

        data = cast("CompareResponse", response.json())

        return data["compare"]["*"]

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # pyright: ignore[reportUnknownParameterType, reportMissingParameterType] # noqa: ANN001
        self.close()
