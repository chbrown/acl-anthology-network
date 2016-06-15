all: out/id_text.tsv out/citingId_citedId.tsv out/id_author_title_venue_year.tsv

aanrelease2013.tar.gz:
	# aanrelease2013.tar.gz is 292 MB, md5: 7d10b490e75b8a22b673173e10fbcc18
	curl -s http://clair.eecs.umich.edu/aan/downloads/aanrelease2013.tar.gz >$@

aan aan/papers_text aan/release/2013/acl.txt aan/release/2013/acl-metadata.txt: | aanrelease2013.tar.gz
	# extract the original tarball, which contains a single directory, aan/
	tar -xzf aanrelease2013.tar.gz

out/id_text.tsv: aan/papers_text
	# flatten all non-empty papers in papers_text/ and concatenate into single file
	# issues:
	# - totally empty papers can cause problems later on (e.g., P02-1046.txt)
	# - there are a lot of other files besides paper texts (e.g., W12-3714.body, collaboration_network.txt)
	# - the content is all over the place, weird whitespace, weird characters
	find $< -name '???-????.txt' -size +1 | xargs -n 1 dev/print_id_text.sh >$@

out/citingId_citedId.tsv: aan/release/2013/acl.txt
	# acl.txt uses ' ==> ' to separate the two IDs, which seems arbitrary
	# the first item generally has a more recent year than the second, so we
	# know the "left ==> right" notation means "citing ==> cited"
	# otherwise it's just ASCII, so that's nice
	<$< awk -F ' ==> ' '{print $$1"\t"$$2}' >$@

out/id_author_title_venue_year.tsv: aan/release/2013/acl-metadata.txt
	# acl-metadata.txt provides some nice metadata, but with an atrocious hodgepodge of encodings.
	# it uses html entities for some non-ASCII characters, and ISO-8859-2 for others,
	# and even some html entity references that aren't html-spec compliant
	# and not only does it use html entities to encode accents, it uses them to encode broken 'mojibaked' accents
	# ftfy from https://github.com/LuminosoInsight/python-ftfy is brilliant.
	# otherwise, the format is pretty straightforward, though some of the key-val pairs span multiple lines
	<$< dev/print_id_author_title_venue_year.py >$@
