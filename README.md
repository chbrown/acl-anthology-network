## ACL Anthology Network derivatives

`aanrelease2013.tar.gz` is a mess.

1. Encodings are all over the place.
2. Some data is obviously missing, or present but corrupted.
3. It's unclear which files are the raw data and which are statistics derived from those data.
4. Files that look like they should be the outputs of scripts are actually the help messages of those scripts.

`Makefile` declaratively provides some documentation of the issues and the cleanup work involved.

This repository does not contain any of the original data, only a programmatic description of how to fix it.

To run, call `make` in the root directory.
