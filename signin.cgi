#!/usr/bin/perl -wT
require './logfile_helper.pl';
require './collection_helper.pl';

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

my $safe_characters = "a-zA-Z0-9_.-";

my $query = new CGI;
my $username = $query->param("username");

open(FP,"signin.html");
my @all_html = readline(FP);
close(FP);
print $query->header ( );

# Make sure username is ok:
if($username) {
    if ( $username =~ /^([$safe_characters]+)$/ ) {
	$username = $1;
    }
    else {
	foreach my $i (@all_html) {
	    if($i eq "<div id=\"msgs\"></div>\n") {
		$i =~ s/<\/div>/<p><font color=\"red\">Invalid character detected.  Please use only letters and numbers.<\/font><\/p><\/div>/;
	    }
	    print $i;
	}
	exit(0);
    }
    
    open(FP,"Logs/usernames.txt");
    my @all_users = readline(FP);
    close(FP);

    my $user_exist = 0;
    foreach my $i (@all_users) {
	$i =~ s/\n//;
	if($i eq $username) {
	    $user_exist = 1;
	}
    }
    if(!$user_exist) {
	foreach my $i (@all_html) {
	    if($i eq "<div id=\"msgs\"></div>\n") {
		$i =~ s/<\/div>/<p><font color=\"red\">This user does not exist.  Please try again or create a new account.<\/font><\/p><\/div>/;
	    }
	    print $i;
	}
	exit(0);
    }
}
else {
    foreach my $i (@all_html) {
	if($i eq "<div id=\"msgs\"></div>\n") {
	    $i =~ s/<\/div>/<p><font color=\"red\">Please enter a username.<\/font><\/p><\/div>/;
	}
	print $i;
    }
    exit(0);
}

# Write to logfile
#my $datestr2 = &GetTimeStamp;
#my $addr = $ENV{'REMOTE_ADDR'};
#open(FP,">>Logs/logfile.txt");
#print FP "\n$datestr2 $addr *upload_image Images/$upload_dir/$filename.jpg";
#close(FP);

&WriteMainCollectionPage($username,"");
