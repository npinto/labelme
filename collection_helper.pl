#!/usr/bin/perl
#

sub WriteMainCollectionPage {

    my($username,$msg) = @_;

    my $randnum = int(rand(999999999)+1);

    # Get all collections:
    opendir(DIR,"./Images/users/$username") || die("Cannot read collections");
    my @all_collections = readdir(DIR);
    closedir(DIR);


    open(FP,"view_all_collections.html");
    my @all_html = readline(FP);
    close(FP);
    
    my $ncols = 0;
    foreach my $a (@all_html) {
	if($a eq "<div id=\"collection_data\"></div>\n") {
	    print "<div style=\"position:relative;width:100%;height:100%;overflow:auto;background-color:#dddddd;border:1px solid #000000;\"><table style=\"width:100%;\" width=\"100%\" cellspacing=\"5\">";
	    foreach my $i (@all_collections) {
		unless(($i eq ".") || ($i eq "..")) {
		    # Get number of images:
		    opendir(DIR,"./Images/users/$username/$i") || die("Cannot read this collection");
		    my @all_images = readdir(DIR);
		    closedir(DIR);
		    my $num_images = scalar(@all_images)-2;
		    if($num_images==1) {
			$num_images = "1 image";
		    }
		    else {
			$num_images = "$num_images images";
		    }
		    
		    # Get number of polygons:
		    my $num_anno_file = 0;
		    my $num_poly = 0;
		    foreach my $j (@all_images) {
			unless(($j eq ".") || ($j eq "..")) {
			    $j =~ s/jpg$/xml/;
			    open(FP,"./Annotations/users/$username/$i/$j") || die($j);
			    my @anno_xml = readline(FP);
			    close(FP);
			    my $num_file_poly = 0;
			    foreach my $k (@anno_xml) {
				my @s = split("<object>",$k);
				$num_file_poly = scalar(@s)-1 + $num_file_poly;
			    }
			    if($num_file_poly) {
				$num_anno_file = $num_anno_file+1;
				$num_poly = $num_poly + $num_file_poly;
			    }
			}
		    }
		    if($num_anno_file==1) {
			$num_anno_file = "1 annotation file";
		    }
		    else {
			$num_anno_file = "$num_anno_file annotation files";
		    }
		    if($num_poly==1) {
			$num_poly = "1 polygon";
		    }
		    else {
			$num_poly = "$num_poly polygons";
		    }
		    
		    if($ncols==0) {
			print "<tr>";
		    }
		    print "<td>$i<br /><table><tr><td>&nbsp;&nbsp;&nbsp;<a href=\"view_collection.cgi?username=$username&collection=$i\"><img src=\"CollectionThumbs/users/$username/$i/main_thumb.jpg?v=$randnum\" style=\"border: 1px solid #979797;\" border=\"0\" width=\"64\" height=\"64\" /></a></td><td>$num_images<br />$num_anno_file<br />$num_poly</td></tr></table></td>";
		    $ncols = ($ncols+1)%4;
		    if($ncols==0) {
			print "</tr>";
		    }
		}
	    }
	    if($ncols != 0) {
		for(my $b=$ncols; $b<4; $b++) {
		    print "<td></td>";
		}
		print "</tr>";
	    }
	    print "</table></div>";
	}
	elsif($a eq "<input type=\"hidden\" />\n") {
	    print "<input type=\"hidden\" name=\"username\" value=\"$username\" />";
	}
	elsif($a eq "<div id=\"username\"></div>\n") {
	    print "$username";
	}
	elsif(($a eq "<div id=\"msgs\"></div>\n") && !($msg eq "")) {
	    print "<div style=\"position:relative;\"><p><font color=\"red\">$msg</font></p></div>";
	}
	else {
	    print $a;
	}
    }
}


sub WriteViewCollectionPage {

    my($username,$collection) = @_;

    my $upload_url = "http://csail.mit.edu/~brussell/research/labelme_upload/upload3D.html";
#    my $upload_url = "http://csail.mit.edu/~brussell/research/labelme_upload/TEST/upload3D.html";
    my $randnum = int(rand(999999999)+1);

    open(FP,"view_collection.html");
    my @all_html = readline(FP);
    close(FP);

    # Check to see if collection exists already:
    opendir(DIR,"./Images/users/$username/$collection") || die("Cannot read collections");
    my @all_images = readdir(DIR);
    closedir(DIR);
    
    my $num_images = scalar(@all_images)-2;
    if($num_images==1) {
	$num_images = "1 image";
    }
    else {
	$num_images = "$num_images images";
    }
    
    # Get number of polygons:
    my $num_anno_file = 0;
    my $num_poly = 0;
    foreach my $j (@all_images) {
	unless(($j eq ".") || ($j eq "..")) {
	    my $xml_file = $j;
	    $xml_file =~ s/jpg$/xml/;
	    open(FP,"./Annotations/users/$username/$collection/$xml_file") || die($xml_file);
	    my @anno_xml = readline(FP);
	    close(FP);
	    my $num_file_poly = 0;
	    foreach my $k (@anno_xml) {
		my @s = split("<object>",$k);
		$num_file_poly = scalar(@s)-1 + $num_file_poly;
	    }
	    if($num_file_poly) {
		$num_anno_file = $num_anno_file+1;
		$num_poly = $num_poly + $num_file_poly;
	    }
	}
    }
    if($num_anno_file==1) {
	$num_anno_file = "1 annotation file";
    }
    else {
	$num_anno_file = "$num_anno_file annotation files";
    }
    if($num_poly==1) {
	$num_poly = "1 polygon";
    }
    else {
	$num_poly = "$num_poly polygons";
    }
    
    my $ncols = 0;
    foreach my $a (@all_html) {
	if($a eq "<div id=\"collection_data\"></div>\n") {
	    print "<div style=\"position:absolute;top:3em;background-color:#aaaa00;padding:0.5em;\">$collection</div><div style=\"position:absolute;top:5em;width:100%;height:100%;overflow:auto;background-color:#dddddd;border:1px solid #000000;\"><p>&nbsp;&nbsp;&nbsp;&nbsp;$num_images, $num_anno_file, $num_poly</p><table style=\"width:100%;\" width=\"100%\" cellspacing=\"20\">";
		foreach my $i (@all_images) {
		    unless(($i eq ".") || ($i eq "..")) {
			if($ncols==0) {
			    print "<tr>";
			}
			print "<td><a href=\"tool.html?mode=c&username=$username&collection=$collection&folder=users/$username/$collection&image=$i\"><img src=\"CollectionThumbs/users/$username/$collection/$i\" border=\"0\" /></a></td>";
			$ncols = ($ncols+1)%8;
			if($ncols==0) {
			    print "</tr>";
			}
		    }
		}
	    if($ncols != 0) {
		for(my $b=$ncols; $b<8; $b++) {
		    print "<td></td>";
		}
		print "</tr>";
	    }
	    print "</table></div>";
	}
	elsif($a eq "<a>Upload an image to this collection</a>\n") {
	    print "<a href=\"$upload_url?username=$username&collection=$collection\">Upload an image to this collection</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href=\"signin.cgi?username=$username\">Return to collections</a>";
	}
	elsif($a eq "<input type=\"hidden\" />\n") {
	    print "<input type=\"hidden\" name=\"username\" value=\"$username\" />";
	}
	elsif($a eq "<div id=\"username\"></div>\n") {
	    print "$username";
	}
	else {
	    print $a;
	}
    }
}

1;
