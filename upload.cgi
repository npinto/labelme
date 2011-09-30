#!/usr/bin/perl -wT
require './logfile_helper.pl';

use strict;
use CGI;
use CGI::Carp qw ( fatalsToBrowser );
use File::Basename;
use File::Copy;
use Image::Magick;

$CGI::POST_MAX = 1024 * 5000;

my $view_collection_url = "http://old-labelme.csail.mit.edu/view_collection.cgi";
#my $view_collection_url = "http://old-labelme.csail.mit.edu/developers/brussell/LabelMe-video/view_collection.cgi";
my $upload_dir = "static_submitted_3d";

my $safe_filename_characters = "a-zA-Z0-9_.-";

my $query = new CGI;
my $image_filename = $query->param("photo");
my $username = $query->param("username");
my $folder = $query->param("folder");
my $author = $query->param("author");
my $description = $query->param("description");
my $include_fname = $query->param("include_fname");

if ( !$image_filename ) {
 print $query->header ( );
 print "There was a problem uploading your photo (try a smaller file).";
 exit;
}

my ( $name, $path, $extension ) = fileparse ( $image_filename, '\..*' );

if ( ($extension ne '.jpg') && ($extension ne '.jpeg') && 
     ($extension ne '.JPG') && ($extension ne '.JPEG') ) {
    print $query->header ( );
    print "The file extension must be jpg ($extension)";
    exit;
}

# Make sure username is ok:
if($username) {
#    $username =~ s/[^$safe_filename_characters]//g;

    if ( $username =~ /^([$safe_filename_characters]+)$/ ) {
	$username = $1;
    }
    else {
	die "Username contains invalid characters";
    }
}
else {
    die "Need to enter username";
}

# Make sure folder name is ok:
if($folder) {
#    $folder =~ s/[^$safe_filename_characters]//g;

    if ( $folder =~ /^([$safe_filename_characters]+)$/ ) {
	$folder = $1;
    }
    else {
	die "Folder name contains invalid characters";
    }
}
else {
    die "Need to enter folder name";
}

# Make sure author is ok:
if($author) {
    $author =~ s/[^$safe_filename_characters\s]//g;

    if ( $author =~ /^([$safe_filename_characters\s]+)$/ ) {
	$author = $1;
    }
    else {
	die "Author contains invalid characters";
    }
}

# Make sure description is ok:
if($description) {
    $description =~ s/[^$safe_filename_characters\s]//g;

    if ( $description =~ /^([$safe_filename_characters\s]+)$/ ) {
	$description = $1;
    }
    else {
	die "Description contains invalid characters";
    }
}

$upload_dir = "users/$username/$folder";

# Make filename a random 10-digit number:
my $filename = "img_" . int(rand(999999999)+1);
while(-e "./Images/$upload_dir/$filename.jpg") {
    $filename = "img_" . int(rand(999999999)+1);
}

# Write to logfile
my $datestr2 = &GetTimeStamp;
my $addr = $ENV{'REMOTE_ADDR'};
open(FP,">>Logs/logfile.txt");
print FP "\n$datestr2 $upload_dir $filename $addr *upload_image $username";
close(FP);

# Get photo:
my $tmp_image_dir = "TmpImages";
my $upload_filehandle = $query->upload("photo");

#open ( UPLOADFILE, ">./Images/$upload_dir/$filename.jpg" ) or die "$!";
open ( UPLOADFILE, ">./$tmp_image_dir/$username\_\_$folder\_\_$filename.jpg" ) or die "$!";
binmode UPLOADFILE;

while ( <$upload_filehandle> ) {
    print UPLOADFILE;
}

close UPLOADFILE;

# Check if photo is valid and create thumbnail:
my $image = Image::Magick->new;
$image->Read("./$tmp_image_dir/$username\_\_$folder\_\_$filename.jpg");
$image->Resize(geometry=>'64x64',width=>64,height=>64,filter=>'Gaussian',support=>5,blur=>1);
$image->Write("./CollectionThumbs/$upload_dir/$filename.jpg");
unless(copy("./CollectionThumbs/$upload_dir/$filename.jpg","./CollectionThumbs/$upload_dir/main_thumb.jpg")) {
    open(FP,"upload3D.html");
    my @all_html = readline(FP);
    close(FP);
    print $query->header ( );
    foreach my $i (@all_html) {
	if($i eq "<div id=\"msgs\"></div>\n") {
	    $i =~ s/<\/div>/<p><font color=\"red\">There was a problem with uploading your JPG file.  Please try again.  If this persists, please <a href=\"http:\/\/people.csail.mit.edu\/torralba\/research\/LabelMe\/js\/AboutMe.html\">contact us<\/a>.<\/font><\/p><\/div>/;
	}
	elsif($i eq "ParseURL();\n") {
	    $i = "";
	}
	elsif($i eq "document.getElementById('username').value = username;\n") {
	    $i = "document.getElementById('username').value = $username;\n";
	}
	elsif($i eq "document.getElementById('collection').value = collection;\n") {
	    $i = "document.getElementById('collection').value = $folder;\n";
	}
	elsif($i eq "<input type=\"hidden\" id=\"username\" name=\"username\" value=\"\" \/>\n") {
	    $i = "<input type=\"hidden\" id=\"username\" name=\"username\" value=\"$username\" \/>\n";
	}
	elsif($i eq "<input type=\"hidden\" id=\"collection\" name=\"folder\" value=\"\" \/>\n") {
	    $i = "<input type=\"hidden\" id=\"collection\" name=\"folder\" value=\"$folder\" \/>\n";
	}
	print $i;
    }
    exit(0);
}

move("./$tmp_image_dir/$username\_\_$folder\_\_$filename.jpg","./Images/$upload_dir/$filename.jpg") or die "$!";

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
print ANNOFILE "<submittedBy>";
print ANNOFILE "$username";
print ANNOFILE "</submittedBy>";
print ANNOFILE "<author>";
print ANNOFILE "$author";
print ANNOFILE "</author>";
print ANNOFILE "<description>";
print ANNOFILE "$description";
print ANNOFILE "</description>";
if($include_fname) {
    print ANNOFILE "<originalFilename>";
    print ANNOFILE "$image_filename";
    print ANNOFILE "</originalFilename>";
}
print ANNOFILE "</source>";
print ANNOFILE "</annotation>";
close ANNOFILE;

# Send user to labeling tool page:
print $query->header ( );
print <<END_HTML;
<html>
<head>
<META HTTP-EQUIV="Refresh" CONTENT="0; URL=$view_collection_url?username=$username&collection=$folder">
</head>
</html>
END_HTML
