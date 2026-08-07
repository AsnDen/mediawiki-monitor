# Mediawiki monitor

Base mediawiki wikis statistics monitor. Uses mediawiki API to get data.

Allows to view general wiki statistics (mainly from `Special:Statistics`).
Provides links to main `Special:` wiki pages,
as well as to `Mediawiki:Common.css` and `Mediawiki:Common.js` pages.

Shows a list of active users and administrators (sysops and bureaucrats).
Also shows a list of installed extensions.

There is a list of recent changes for each wiki.
It's possible to see their diffs (for articles) and author.

Each author page shows a list or their recent contributions.

## How to setup and run

You can edit `config.py` file to add your wikis.
The key is wiki id (any possible value),
the value is the url to wiki's `api.php` file.

The main way to run is by using Docker.

Simply rin `run.bat` or `run.sh`. You can use Docker flags with these runners.
For example:

```shell
./rundev.sh -d
```

## Future

1. Support for mediafiles.
1. User's statistics and contribution.
1. Support for user-defined wikis.
1. Search for text/page in all wikis at once.
1. Saving some wiki data in database for future use.
1. Hub where multiple wiki statistics will be at once (user defined).
1. Better styles and user-defined styles.
1. Translation.
