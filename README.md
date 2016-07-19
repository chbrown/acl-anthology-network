## ACL Anthology Network derivatives

`aanrelease2013.tar.gz` is a mess.

1. Encodings are all over the place.
2. Some data is obviously missing, or present but corrupted.
3. It's unclear which files are the raw data and which are statistics derived from those data.
4. Files that look like they should be the outputs of scripts are actually the help messages of those scripts.
5. Many of the `papers_text/` files (plain text extracted from the PDF) have issues:
  * Some are gibberish due to non-compliant PDF encoding (e.g., `P00-1032`, `W06-3709`)
  * Others are gibberish to varying degrees, due to bad OCR in the original PDF (from problematic, e.g., `T75-2033`, to unusable, e.g., `J79-1013`)
  * Others are not in English (e.g., `C73-2029`)
  * Others contain the text of a completely different paper (e.g., `L08-1302`)

`Makefile` declaratively provides some documentation of the issues and the cleanup work involved.

This repository does not contain any of the original data, only a programmatic description of how to fix it.

To run, call `make` in the root directory.


## Summary statistics

The [University of Michigan](http://umich.edu/) [CLAIR Group](http://clair.si.umich.edu/clair/homepage/)'s [ACL Anthology Network interface](http://clair.eecs.umich.edu/aan/index.php) reports the following statistics:

| Measure                         |   Value |
|:--------------------------------|--------:|
| Number of papers                |  21,212 |
| Number of authors               |  17,792 |
| Number of venues                |     342 |
| Number of paper citations       | 110,975 |
| Number of author collaborations | 142,450 |
| Citation network diameter       |      22 |
| Collaboration network diameter  |      15 |

Some of these are inaccurate, or describe only one of the data sources.
Different sources in the dataset contain different subsets of the data; for example, citations are reported for some papers that do not have a corresponding `papers_text/` file (e.g., `L08-1098`).

### `aan/release/2013/acl.txt`

<!-- # setup:
awk -F ' ==> ' '{print $1}' acl.txt | sort > citing.txt
awk -F ' ==> ' '{print $2}' acl.txt | sort > cited.txt
awk -F $'\t' '{print $2}' out/id_author_title_venue_year.tsv | sed $'s/; */\\\n/g' > out/authors.txt
-->

| Measure                                    |   Value |
|:-------------------------------------------|--------:|
| citing→cited relationships                 | 110,930 | <!-- wc -l acl.txt -->
| unique citing papers                       |  16,554 | <!-- uniq citing.txt | wc -l -->
| avg. cited per citing                      |  6.7011 | <!-- 110930 / 16554 -->
| unique cited papers                        |  12,840 | <!-- uniq cited.txt | wc -l -->
| avg. citing per cited                      |  8.6394 | <!-- 110930 / 12840 -->
| unique papers                              |  18,160 | <!-- sort citing.txt cited.txt | uniq | wc -l -->
| unique papers that both cite and are cited |  11,234 | <!-- comm -1 -2 <(uniq citing.txt) <(uniq cited.txt) | wc -l -->
| unique author names                        |  16,786 | <!-- sort out/authors.txt | uniq | wc -l -->


| Top 10 most-cited papers | # of papers citing | authors         | title |
|-------------------------:|-------------------:|:----------------|:------|
|                 J93-2004 |                928 | Mitchell et al. | Building A Large Annotated Corpus Of English: The Penn Treebank Computational Linguistics | <!-- sort cited.txt | uniq -c | sort -g | tail -10r -->
|                 P02-1040 |                891 | Papineni et al. | Bleu: A Method For Automatic Evaluation Of Machine Translation |
|                 J93-2003 |                729 | Brown et al.    | The Mathematics Of Statistical Machine Translation: Parameter Estimation |
|                 P03-1021 |                667 | Och & Josef     | Minimum Error Rate Training In Statistical Machine Translation |
|                 J03-1002 |                656 | Och & Josef     | A Systematic Comparison Of Various Statistical Alignment Models |
|                 P07-2045 |                591 | Koehn et al.    | Moses: Open Source Toolkit for Statistical Machine Translation |
|                 N03-1017 |                556 | Koehn et al.    | Statistical Phrase-Based Translation |
|                 P03-1054 |                394 | Klein & Manning | Accurate Unlexicalized Parsing |
|                 J96-1002 |                376 | Berger et al.   | A Maximum Entropy Approach To Natural Language Processing |
|                 A00-2018 |                371 | Charniak        | A Maximum-Entropy-Inspired Parser |


| Top 10 most-citing papers | # of papers cited |
|--------------------------:|------------------:|
|                  P10-1142 |                88 | <!-- sort citing.txt | uniq -c | sort -g | tail -10r -->
|                  J10-3003 |                80 |
|                  W13-4917 |                71 |
|                  W13-2201 |                65 |
|                  J12-1006 |                62 |
|                  J98-1001 |                59 |
|                  J13-2003 |                59 |
|                  J07-4004 |                57 |
|                  J11-2002 |                52 |
|                  D11-1108 |                52 |


### `aan/release/2013/acl-metadata.txt`

The formatting of this file is, frankly, befuddling. The general structure is BibTeX-esque, but no BibTeX parser could possibly handle it. Worse, the mixture of encodings is insane! If [`ftfy`](https://github.com/LuminosoInsight/python-ftfy) was ever looking for a great real-world case study, this would be it.

<!-- echo $'id\tauthor\ttitle\tvenue\tyear' | cat - out/id_author_title_venue_year.tsv | synopsize -->

* There are 20,989 papers.
* There is 1 missing `author`, `W10-4238`, and 16,308 unique `author` sequences (`author` lists all authors for that paper).
* There are 12 missing venues, and 494 unique venue values.
* The year field ranges from 1965 to 2013, with 41 unique values (there are some gaps prior to 1978).
* There are 18,152 papers (all but 8) in the citation network that have an entry in this metadata file
* Of the 110,930 total edges in the citation network, 110,889 have entries in this metadata file.


### `aan/papers_text/???-????.txt`

There are a lot of other files in this directory; some of the papers are segmented into body and references sections; there are some files that seem like they were intended to go in `aan/release/2013/`; and many of the files that match this pattern are empty.

* There are 20,194 files that match that pattern and are non-empty.
* There are 17,593 papers in the citation network that have a corresponding file in `papers_text/`.
* Of the 110,930 total edges in the citation network, 107,873 have corresponding files in `papers_text/`.


## Credits

Despite these flaws, the ACL Anthology Network is a great resource;
many thanks to the [many contributors](http://clair.eecs.umich.edu/aan/about.php).

> Dragomir R. Radev, Pradeep Muthukrishnan, Vahed Qazvinian, Amjad Abu-Jbara. 2013. The ACL Anthology Network Corpus. Language Resources and Evaluation 47 (4), pp. 919–944. [10.1007/s10579-012-9211-2](http://dx.doi.org/10.1007/s10579-012-9211-2).


## License

Copyright 2016 Christopher Brown. [MIT Licensed](http://chbrown.github.io/licenses/MIT/#2016).
