#!/usr/bin/perl -wT

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;

$CGI::POST_MAX = 1024 * 5000;

my $safe_filename_characters = "a-zA-Z0-9_.-";

my $upload_dir = "static_submitted_3d";
#my $upload_dir = "./Images/static_submitted_3d";
#my $upload_dir = "./upload_test";

my $query = new CGI;
my $filename = $query->param("photo");
my $username = $query->param("username");

if ( !$filename ) {
 print $query->header ( );
 print "There was a problem uploading your photo (try a smaller file).";
 exit;
}

my ( $name, $path, $extension ) = fileparse ( $filename, '\..*' );

if ( ($extension ne '.jpg') && ($extension ne '.jpeg') && 
     ($extension ne '.JPG') && ($extension ne '.JPEG') ) {
    print $query->header ( );
    print "The file extension must be jpg ($extension)";
    exit;
}

#$filename = $name;

#$filename =~ tr/ /_/;
#$filename =~ s/[^$safe_filename_characters]//g;

#if ( $filename =~ /^([$safe_filename_characters]+)$/ ) {
# $filename = $1;
#}
#else {
# die "Filename contains invalid characters";
#}

# Make sure username is ok:
if($username) {
    $username =~ s/[^$safe_filename_characters\s]//g;

    if ( $username =~ /^([$safe_filename_characters\s]+)$/ ) {
	$username = $1;
    }
    else {
	die "Username contains invalid characters";
    }
}

# Make filename a random 10-digit number:
$filename = "img_" . int(rand(999999999)+1);

# Get photo:
my $upload_filehandle = $query->upload("photo");

open ( UPLOADFILE, ">./Images/$upload_dir/$filename.jpg" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle> )
{
 print UPLOADFILE;
}

close UPLOADFILE;

# Write username to annotation file:
open(ANNOFILE,">Annotations/$upload_dir/$filename.xml") or die "$!";
print ANNOFILE "<annotation>";
print ANNOFILE "<filename>";
print ANNOFILE "$filename.jpg";
print ANNOFILE "</filename>";
print ANNOFILE "<folder>";
print ANNOFILE "$upload_dir";
print ANNOFILE "</folder>";
print ANNOFILE "<source>";
print ANNOFILE "<sourceImage>";
print ANNOFILE "submitted";
print ANNOFILE "</sourceImage>";
print ANNOFILE "<sourceAnnotation>";
print ANNOFILE "LabelMe Webtool";
print ANNOFILE "</sourceAnnotation>";
if($username) {
    print ANNOFILE "<submittedBy>";
    print ANNOFILE "$username";
    print ANNOFILE "</submittedBy>";
}
print ANNOFILE "</source>";
print ANNOFILE "</annotation>";
close ANNOFILE;

# Send user to labeling tool page:
print $query->header ( );
print <<END_HTML;
<html>
<head>
<META HTTP-EQUIV="Refresh"
CONTENT="0; URL=http://labelme.csail.mit.edu/tool.html?collection=LabelMe&mode=i&folder=static_submitted_3d&image=$filename.jpg">
</head>
</html>
END_HTML
