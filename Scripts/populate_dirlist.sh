#!/bin/sh
#
# populate_dirlist.sh
# <brussell@csail.mit.edu>
# Created: 02/01/2006
# Updated: 03/10/2006
# Updated: 05/02/2006 <sdavies@mit.edu>
# Updated: 05/21/2007

# Change output filename if desired.  Note that labelme.txt
# must exist for the bare system to work.
dirlist_fname='labelme.txt'

# Add any options here: 
ImageDirWildcards=""
#ImageDirWildcards="| grep -v seq"
#ImageDirWildcards="| grep june"

# Target directories where images are and where output
# dirlist will be put.
ImageDir='./Images'
DirListsDir='./DirLists'

# Code starts here:
currdir=$(pwd)

if [ -d $DirListDir ]; then

touch $currdir/$DirListsDir/$dirlist_fname

find $ImageDir -maxdepth 1 -mindepth 1 -type d -follow -name '*' -printf %f\\n $ImageDirWildcards | while read i; do
    echo $i
    cd "$currdir/$ImageDir/$i"
    find . -maxdepth 1 -name '*.jpg' -printf %f\\n | while read j; do
	echo "$i,$j" >> $currdir/$DirListsDir/$dirlist_fname
    done
done

cd $currdir

else
	echo "You need to create the DirList directory"
fi
