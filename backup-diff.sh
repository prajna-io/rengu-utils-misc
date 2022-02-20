#!/bin/sh

DATESTAMP=$( date +"%Y%m%d-%H%M" )

rengu -Bxro:data/xapian show '*' | sort > tmp/old.idx
rengu -Blmr:data/lmdb show '*' | sort > tmp/new.idx

diff tmp/old.idx tmp/new.idx | \
  grep '^>' | awk '{ print $2 }' | \
  xargs -n1 rengu show -ojson > tmp/add-${DATESTAMP}.json

gh gist create -d "Backup ${DATESTAMP}" tmp/add-${DATESTAMP}.json && \
  rm tmp/add-${DATESTAMP}.json
 
