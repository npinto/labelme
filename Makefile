# Makefile
# <brussell@csail.mit.edu>
# Created: 01/30/2006
# Updated: 05/21/2007

# Make these two variables point to where your Images/ Annotations/ 
# TmpAnnotations/ folders are located.
IMAGES_DIR=/afs/csail/group/vision/www/data/LabelMe/Test/Images
ANNOTATIONS_DIR=/afs/csail/group/vision/www/data/LabelMe/Test/Annotations
TMP_ANNOTATIONS_DIR=/afs/csail/group/vision/www/data/LabelMe/Test/TmpAnnotations

all: images annotations tmp_annotations dirlists counter logs labelme3d

annotations:
	if [ -a "Annotations" ]; then echo "ANNOTATIONS_DIR all set."; else ln -s $(ANNOTATIONS_DIR) Annotations; fi;

tmp_annotations:
	if [ -a "TmpAnnotations" ]; then echo "TMP_ANNOTATIONS_DIR all set."; else ln -s $(TMP_ANNOTATIONS_DIR) TmpAnnotations; fi;

images:
	if [ -a "Images" ]; then echo "IMAGES_DIR all set."; else ln -s $(IMAGES_DIR) Images; fi;

dirlists:
	mkdir DirLists
	./Scripts/populate_dirlist.sh

counter:
	touch counter
	touch counter_tmp
	./Scripts/anno_count.sh

logs:
	mkdir Logs
	touch Logs/logfile.txt
	chmod 666 Logs/logfile.txt
#	fs setacl Logs www rliw  # Uncomment for AFS permissions

labelme3d:
	ln -s $(IMAGES_DIR) LabelMe3D/Images
	ln -s $(ANNOTATIONS_DIR) LabelMe3D/Annotations
	ln -s $(TMP_ANNOTATIONS_DIR) LabelMe3D/TmpAnnotations
