# Compare US remakes of foreign shows based on IMDb scores

There have been quite many US remakes from foreign originals but **do they perform better than the originals**?

To examine this, I used the shows listed in the Wikipedia tables of the US remakes of [UK shows](https://en.wikipedia.org/wiki/List_of_American_television_series_based_on_British_television_series) and [foreign shows](https://en.wikipedia.org/wiki/List_of_American_television_shows_based_on_foreign_shows), scraped the available IMDb links from their corresponding Wikipedia pages (in the external link section). Then using the IMDb URLs, I obtained the ratings (scores) data using [`imdbpy`](https://imdbpy.github.io/). Below is the `plotly` figure.

Generally, US remakes perform much worse than the foreign originals in terms of IMDb scores, for both TV series, as well as reality-like shows (like *Dancing with the stars*), except for some popular shows  (eg. *The Office*, *House of Cards* or *Pop idol*, i.e. *American Idol*). Plus, popularity, if measured by the number of votes for IMDb ratings, seems roughly more intense for original shows. There is a positive relationship between score difference and popularity difference as well.

{% include_relative docs/imdb-remakes.html %}

See [notebook](https://nbviewer.jupyter.org/github/tuanpham96/series-remake/blob/main/notebook.ipynb) for more information.

