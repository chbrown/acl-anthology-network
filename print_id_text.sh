#!/usr/bin/env bash
FILENAME=$1
printf "%s\t" $(basename -s .txt $FILENAME)
# tr #1: squeeze everything that isn't an alphanumermic or apostrophe into a literal space
#   nb.: 037 is "U+0027 APOSTROPHE" in octal (I'm not sure that's working, though)
# tr #2: squeeze all sequences of one or more whitespace characters into a single "U+0020 SPACE"
<$FILENAME tr -Cs "[:alnum:]\037" ' ' | tr -s [:space:] ' '
printf "\n"
