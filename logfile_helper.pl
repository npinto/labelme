#!/usr/bin/perl

sub WriteLogfile {
    my($datestr2,$folder,$fname,$tot_before,$tot_after,$addr,$host,$objname,$global_count,$username,$modifiedControlPoints,$tot_del_before,$tot_del_after) = @_;
    open(FP,">>Logs/logfile.txt");
#open(FP2,">>Logs/logfile.xml");
#if($tot_after > $tot_before) {
#    print FP2 "<entry><timestamp>$datestr2</timestamp><folder>$folder</folder><filename>$fname</filename>";
#    print FP2 "<num_poly_before>$tot_before</num_poly_before><num_poly_after>$tot_after</num_poly_after>";
#    print FP2 "<ipaddress>$addr</ipaddress><name_after>$objname</name_after>";
#    print FP2 "<personal_count>$global_count</personal_count><username>$username</username>";
#    print FP2 "<status>CREATED</status></entry>";
#}
#else if($tot_after==$tot_before) {
#    
#    ($objname,$junk) = split("</name>",@poly_split[$tot_after]);
#    ($junk,$objname) = split("<name>",$objname);
#    # Remove spaces from the name:
#    $objname =~ s/\s/_/g;
#    print FP "\n$datestr2 $folder $fname $tot_before $tot_after $addr $objname $global_count $username UPDATED_NAME";
#}
#else {
#    print FP2 "\n$datestr2 $folder $fname $tot_before $tot_after $addr $global_count $username";
#}
    print FP "\n$datestr2 $folder $fname $tot_before $tot_after $addr $host $objname $global_count $username $modifiedControlPoints $tot_del_before $tot_del_after"; #include $ref???
    close(FP);
#close(FP2);
}

sub GetPrivateData {
    my($stdin) = @_;

    # Get the global count:
    ($global_count,$junk) = split("</global_count>",$stdin);
    ($junk,$global_count) = split("<global_count>",$global_count);

    # Get the username:
    ($username,$junk) = split("</pri_username>",$stdin);
    ($junk,$username) = split("<pri_username>",$username);

    # Get the edited flag:
    ($edited,$junk) = split("</edited>",$stdin);
    ($junk,$edited) = split("<edited>",$edited);

    # Get the old_name flag:
    ($old_name,$junk) = split("</old_name>",$stdin);
    ($junk,$old_name) = split("<old_name>",$old_name);

    # Get the new_name flag:
    ($new_name,$junk) = split("</new_name>",$stdin);
    ($junk,$new_name) = split("<new_name>",$new_name);

    # Get the modifiedControlPoints flag:
    ($modifiedControlPoints,$junk) = split("</modified_cpts>",$stdin);
    ($junk,$modifiedControlPoints) = split("<modified_cpts>",$modifiedControlPoints);

    # Check if names are empty:
    if($old_name eq "") {
	$old_name = "*empty*";
    }
    if($new_name eq "") {
	$new_name = "*empty*";
    }

    return ($global_count,$username,$edited,$old_name,$new_name,$modifiedControlPoints);
}

sub GetTimeStamp {
    ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = gmtime(time);
    $monword = (qw(Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec))[$mon];
    $mon = sprintf("%2.2d",$mon+1);
    $mday = sprintf("%2.2d",$mday);
    $year = $year+1900;
    $hour = sprintf("%2.2d",$hour);
    $min = sprintf("%2.2d",$min);
    $sec = sprintf("%2.2d",$sec);

    $datestr = join ':', $mon,$mday,$year,$hour,$min,$sec;

    $datefirst = join '-', $mday,$monword,$year;
    $datesecond = join ':', $hour,$min,$sec;
    $datestr2 = join ' ', $datefirst,$datesecond;
    return $datestr2;
}

sub IsSubmittedXmlOk {
    my($stdin) = @_;

    # Check to make sure $stdin ends with </annotation>:
    $isOK = ($stdin =~ m/<\/annotation>$/);

    return ($isOK);
#    return (0);
}

1;
