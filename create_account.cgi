#!/usr/bin/perl -wT
require './logfile_helper.pl';

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

my $safe_characters = "a-zA-Z0-9_.-";

my $query = new CGI;
my $username = $query->param("username");

open(FP,"create_account.html");
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
    if($user_exist || ($username eq "admin")) {
	foreach my $i (@all_html) {
	    if($i eq "<div id=\"msgs\"></div>\n") {
		$i =~ s/<\/div>/<p><font color=\"red\">This username already exists.  Please choose another username.<\/font><\/p><\/div>/;
	    }
	    print $i;
	}
	exit(0);
    }

    open(FP,">>Logs/usernames.txt");
    print FP "\n$username";
    close(FP);

    mkdir "./Images/users/$username" or die;
    mkdir "./Annotations/users/$username" or die;
    mkdir "./CollectionThumbs/users/$username" or die;
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
my $datestr2 = &GetTimeStamp;
my $addr = $ENV{'REMOTE_ADDR'};
open(FP,">>Logs/logfile.txt");
print FP "\n$datestr2 $addr *account_created $username";
close(FP);

# Send user to labeling tool page:
print <<END_HTML;
<html>
<head>
<META HTTP-EQUIV="Refresh" CONTENT="0; URL=signin.cgi?username=$username">
</head>
</html>
END_HTML
