#!/usr/bin/perl

# Record the time into logfile:

# Get the time:
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

$addr = $ENV{'REMOTE_ADDR'};
$host = $ENV{'REMOTE_HOST'};

# write download counter:
open(FP,">>Logs/download_counter.txt");
print FP "STARTING-STREAM: $datestr2 $addr $host\n";

# Send stream:
open ZIP, "tar -ch Annotations/ | gzip -c |";
print "Content-type: application/x-gzip\n" ;
print "Content-Disposition: attachment; filename=Annotations.tar.gz\n\n";
print <ZIP>;
close ZIP; 

print FP "FINISHED-STREAM: $datestr2 $addr $host\n";
close(FP);

## some google groups comments:

#> Is it possible to send the result of zip command directly for
#> printing in the browser, so the download take place without a
#> temporary file?

#Sure.  This would be the easiest solution, as it eliminates the whole
#issue of temporary files and cleaning up.  Say you gather the list of
#files to zip into @files:

#  my $fl = join ' ', @files;
#  open ZIP, "zip - $fl |";
#  print "Content-type: application/octet-stream\n\n";
#  print <ZIP>;
#  close ZIP; 

