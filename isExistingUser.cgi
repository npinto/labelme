#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

my $safe_characters = "a-zA-Z0-9_.-";

my $query = new CGI;
my $username = $query->param("username");

# Make sure username is ok:
my $user_exist = 0;
if($username) {
    open(FP,"Logs/usernames.txt");
    my @all_users = readline(FP);
    close(FP);

    foreach my $i (@all_users) {
	$i =~ s/\n//;
	if($i eq $username) {
	    $user_exist = 1;
	}
    }
}

# Send user to labeling tool page:
print "Content-type: text/xml\n\n";
print "<user_exist>$user_exist</user_exist>";
