#!/usr/local/bin/perl
#addes missing <id> tags
#fixes <id> tags that are not sequentially ordered, starting at 0

$file = $ARGV[0];
print "-------------$file----------\n";
open(IN,$file);
my $xml = do { local $/; <IN>}; #load the whole file at once
@objects = split(/<object>/,$xml);
@findlist = ();
@replacelist = ();

#1. figure out what ids need to be replaced (push them onto the find/replace lists)
#2. add ids that are missing

my $current_id = 0;
my $new_xml = $objects[0];

for($i=1;$i<=$#objects;$i++) {
    $obj = $objects[$i];
    my $name = 0;
    if($obj =~ /<name>\s*([^\/]+)\s*<\/name>/i) {
	$name = $1;
    }
#    if($i == 1 && $name ne "chair") {
#	print "*** first object in $file is not \"chair\"\n";
#    }
    if($obj =~ /<id>\s*([^\/]+)\s*<\/id>/i) {
	$this_id = $1;
        if($current_id ne $this_id) {
	    print "object \"$name\" has id: \"$this_id\" but should have id \"$current_id\"\n";
	    push(@findlist,$this_id);
	    push(@replacelist,$current_id);
        }
	$new_xml = $new_xml."<object>".$obj;
    }
    else {
	print "object \"$name\" has no id but should have id \"$current_id\"\n";
	$new_xml = $new_xml."<object><id>TEMPORARY_DISTINGUISHER$current_id</id>".$obj;
    }
    $current_id ++;
}


$_ = $new_xml;

for($i=0;$i<=$#findlist;$i++) {
    s/<id>\s*$findlist[$i]\s*<\/id>/<id>TEMPORARY_DISTINGUISHER$replacelist[$i]<\/id>/ig;
    s/<parent>\s*$findlist[$i]\s*<\/parent>/<parent>TEMPORARY_DISTINGUISHER$replacelist[$i]<\/parent>/ig;
}
s/TEMPORARY_DISTINGUISHER//ig;

$new_xml = $_;

open(OUT,">$file");

print OUT $new_xml;
