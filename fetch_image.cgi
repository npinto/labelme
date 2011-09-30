#!/usr/bin/perl

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );

my $query = new CGI;
my $mode = $query->param("mode");
my $username = $query->param("username");
my $collection = $query->param("collection");
my $folder = $query->param("folder");
my $image = $query->param("image");

my $im_dir;
my $im_file;
if($mode eq "i") {
    my $fname = "DirLists/$collection.txt";
    
    if(!open(FP,$fname)) {
	print "Status: 404\n\n";
	return;
    }
    
    open(NUMLINES,"wc -l $fname |");
    my $numlines = <NUMLINES>;
    ($numlines,my $bar) = split(" DirLists",$numlines);
    close(NUMLINES);
    
    my $line = int(rand($numlines))+1;
    
    for(my $i=1; $i < $line; $i++) {
	my $garbage = readline(FP);
    }
    
    my $fileinfo = readline(FP);
    ($im_dir,$im_file) = split(",",$fileinfo);
    $im_file =~ tr/"\n"//d; # remove trailing newline
    
    close(FP);
}
elsif($mode eq "c") {
    opendir(DIR,"./Images/users/$username/$collection") || die("Cannot read collections");
    my @all_images = readdir(DIR);
    closedir(DIR);

    my $c = 0;
    foreach my $i (@all_images) {
	if($i eq $image) {
	    goto next_section;
	}
	$c = $c+1;
    }
  next_section:
    if($c == scalar(@all_images)-1) {
	$c = 1;
    }
    $im_file = $all_images[$c+1];
    $im_dir = $folder;
}
if($mode eq "f") {
    opendir(DIR,"./Images/$folder") || die("Cannot read folder");
    my @all_images = readdir(DIR);
    closedir(DIR);
    do {
	my $i = int(rand(scalar(@all_images)));
	$im_dir = $folder;
	$im_file = $all_images[$i];
    }
    while(!($im_file =~ m/\.jpg$/))

#    my $fname = "DirLists/$collection.txt";
#    
#    if(!open(FP,$fname)) {
#	print "Status: 404\n\n";
#	return;
#    }
#    
#    open(NUMLINES,"wc -l $fname |");
#    my $numlines = <NUMLINES>;
#    ($numlines,my $bar) = split(" DirLists",$numlines);
#    close(NUMLINES);
#    
#    my $line = int(rand($numlines))+1;
#    
#    for(my $i=1; $i < $line; $i++) {
#	my $garbage = readline(FP);
#    }
#    
#    my $fileinfo = readline(FP);
#    ($im_dir,$im_file) = split(",",$fileinfo);
#    $im_file =~ tr/"\n"//d; # remove trailing newline
#    
#    close(FP);
}

# Send back data:
print "Content-type: text/xml\n\n" ;
print "<out><dir>$im_dir</dir><file>$im_file</file></out>";
