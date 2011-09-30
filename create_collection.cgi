#!/usr/bin/perl -wT
require './logfile_helper.pl';
require './collection_helper.pl';

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use File::Copy;

my $safe_characters = "a-zA-Z0-9_.-";

my $query = new CGI;
my $username = $query->param("username");
my $collection = $query->param("collection");

print $query->header ( );

# Make sure username is ok:
if($username) {
    if ( $username =~ /^([$safe_characters]+)$/ ) {
	$username = $1;
    }
    else {
	die "Username contains invalid characters";
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
	die "User does not exist";
    }
}
else {
    die "Need to enter username";
}

# Make sure collection name is ok:
if($collection) {
    if ( $collection =~ /^([$safe_characters]+)$/ ) {
	$collection = $1;
    }
    else {
	&WriteMainCollectionPage($username,"Invalid character detected.  Please use only letters and numbers.");
	exit(0);
    }

    # Check to see if collection exists already:
    unless(-d "./Images/users/$username/$collection") {
	mkdir "./Images/users/$username/$collection" or die;
    }
    unless(-d "./Annotations/users/$username/$collection") {
	mkdir "./Annotations/users/$username/$collection" or die;
    }
    unless(-d "./CollectionThumbs/users/$username/$collection") {
	mkdir "./CollectionThumbs/users/$username/$collection" or die;
	copy("./CollectionThumbs/empty.jpg","./CollectionThumbs/users/$username/$collection/main_thumb.jpg") or die;
    }
}
else {
    &WriteMainCollectionPage($username,"Please enter a collection name.");
    exit(0);
}

# Write to logfile
my $datestr2 = &GetTimeStamp;
my $addr = $ENV{'REMOTE_ADDR'};
open(FP,">>Logs/logfile.txt");
print FP "\n$datestr2 users/$username/$collection $addr *create_collection $username";
close(FP);

# Send user to labeling tool page:
print <<END_HTML;
<html>
<head>
<META HTTP-EQUIV="Refresh" CONTENT="0; URL=signin.cgi?username=$username">
</head>
</html>
END_HTML
