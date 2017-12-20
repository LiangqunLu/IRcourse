#!/usr/bin/perl -w

#perl ./hw2_1.pl "iris.csv" "output.txt"

use strict;
use warnings;

my $num_args = $#ARGV + 1;

if($num_args != 2){
    
    print("\nUsage: perl name.pl input_file output_file\n");
    exit;
    
}


my ($ifile, $dest) = @ARGV;

open(my $fh, '<', $ifile) or die("Unable to open $ifile: $!\n");

open(my $out, ">", $dest) or die("Unable to open $dest: $!\n");

my $line = 0;

while (my $row = <$fh>) {
 
    chomp $row;
    #print "$row\n";
    print $out "$row\n";
 
    $line += 1; 
}    

print("Copy line numer is :", $line, "\n");

close $fh;
close $out



