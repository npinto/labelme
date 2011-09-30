#!/usr/bin/perl
#use lib '/afs/csail.mit.edu/u/f/fergus/public_html/';
use CGI;
use Mail::Sendmail;
#use strict;

$query = new CGI;

if ($query->param("name") eq "") {
  print "Content-type: text/html\n\n";
  print "Please fill in your name and try again";
  return;
}

if ($query->param("email") eq "") {
  print "Content-type: text/html\n\n";
  print "Please fill in your email and try again";
  return;
}

if ($query->param("organization") eq "") {
  print "Content-type: text/html\n\n";
  print "Please fill in your organization and try again";
  return;
}

my %mail = ( 
	 smtp => 'smtp.csail.mit.edu',
	 from => 'labelme@csail.mit.edu',
	 to   => 'brussell@csail.mit.edu,torralba@csail.mit.edu',
	 subject => 'LabelMe code request',
        );
$mail{Message} =  "Code request from:\t\t" . $query->param("name")
	 . "\nEmail address:    \t\t"
.  $query->param("email") . "\nOrganization:     \t\t"
	 . $query->param("organization"). "\nMailing address:  \t\t"
	 . $query->param("mail_address"). "\nExtra people:     \t\t"
	 . $query->param("extra_people").  "\nSend updates:  \t\t"
	 . $query->param("update").  "\n";

sendmail(%mail) || print "Error: $Mail::Sendmail::error\n";

print "Content-type: text/html\n\n";
print "Thank you for your submission. If approved, you will receive the code within a day or so.";
    
