#!/usr/local/bin/perl
#gets rid of deleted objects

$file = $ARGV[0];
open(IN,$file);
my $xml = do { local $/; <IN>}; #load the whole file at once

@objects = split(/<object>/,$xml);
my $new_xml = $objects[0];
my $deleted_count = 0;
for($i=1;$i<$#objects;$i++) {
    $obj = $objects[$i];
    if($obj =~ /<deleted>\s*1\s*<\/deleted>/i) {
	$deleted_count++;
    }
    else {
	$new_xml .= "<object>" . $obj;
    }
}

$obj = $objects[$#objects];
if($obj =~ /<deleted>\s*1\s*<\/deleted>/i) {
    $new_xml .= "</annotations>";
}
else {
    $new_xml .= "<object>" . $obj;
}

print "removed $deleted_count deleted objects from $file\n";
open(OUT,">$file");

print OUT $new_xml;
