# Mediawiki monitor

Base mediawiki wikis statistics monitor.

## TODO list

### Site itself

1. The main page should have links to subpages of wiki faimilies.
1. Should have several pages for each wiki family `(/wikimonitor/<family>)`
1. Each family page should have statistics for:
    * General wiki statistics (see `/Special:Statistics`)
    * Recent changes block
    * List of active users

1. Each recent changes block should show a list of N recent changes.
1. Each recent change has author, diff links and so on (like mediawiki does in `/Special:RecentChanges`).

1. Each author page has a list of recent changes with ability to see diffs.

### Flask

1. `wikimonitor/<family>` for viewing wiki stat.
1. `wikimoninor/<family>/diff?title=...&diff=...&old_diff=...`
1. `wikimonitor/<family>/<user>`

### Code

1. Class that works with mediawiki api. Can get diffs, authors and so on.

### Future

1. Saving data in sqlite for future use.
