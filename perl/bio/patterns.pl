# patterns.pl
# Version 0.91 by Matt Nash 20 August 2005
# Now with summary files!
# mattnash@intrex.net
# Free for all uses
# Free to modify -- just include this notice
# Syntax: patterns.pl [patlen] [match_thresh] [input filename] [output file prefix]
#
#
# patlen: number of fixed positions to use in generated patterns
# match_thresh: number of matches required before we are interested in a particular generated regex
# [input filename]: A file containing your sequences of any type, one per line
# [output file prefix] -- a number indicating the number of residues in the pattern
# will be appended, along with a ".txt" file extension, to the value here


use strict;
use IO::File;
use Math::Combinatorics;

#Change default values here
my $patlen = 3;  #The number of residues in our patterns
my $match_thresh = 5;	#The number of matches required before we include it in our output file
my $infile = "mntestsetin"; #The input file
my $outfile = "matches-$patlen"; #The output file

#Change input and output paths here
my $inpath = "C:\\perl\\";
my $outpath = $inpath;

if (!(@ARGV)) {
	print 	"Using default values:\n" .
		"    Positions: $patlen\n" .
		" Min. matches:	$match_thresh\n" .
		"   Input file:	$infile\n" .
		"  Output file:	$outfile\n";
	sleep 3;
} else {
	$patlen = shift @ARGV;
	$match_thresh = shift @ARGV if (@ARGV);
	$infile = shift @ARGV if (@ARGV);
	$outfile = shift @ARGV if (@ARGV);
}

$outfile .= "-$patlen.txt"

my %matches;
my %matchcount;

my $outfile = "matches-$patlen.txt";
my $sumfile = "summary-$patlen.txt";

my $infh = new IO::File;
my $input = $inpath . $infile;
$infh->open("<$input") or die "Couldn't open $input for reading\n";

my @sequences;
my $maxlen=0;

print "Reading input sequences";
while (my $line = <$infh>) {
	chomp $line;
	next if (grep /$line/, @sequences); #eliminate duplicate sequences
	push @sequences, $line;
	my $linelen = length $line;
	$maxlen = $linelen unless ($maxlen > $linelen);
	print ".";
}

my $numseqs = @sequences;

$infh->close();
print "\n$numseqs sequences read of max length $maxlen\n";

my @positions;
my @patterns;
foreach my $i (0..$maxlen-1) {
	push @positions, $i;
	}

my $combinat = Math::Combinatorics->new(count => $patlen,
					data => [@positions],
					);
my $idx = 0;
print "Generating patterns...\n";
while (my @cur_pat = $combinat->next_combination) {
	push @{ $patterns[$idx] }, @cur_pat;
	$idx++;
	}
my $numpats = @patterns;
print "$numpats patterns generated!\n";
sleep 2;

my $regexcount=0;

print "Processing sequences\n";
SEQ: foreach my $curseq (@sequences) { #loop through sequences
	my $regexsubt = 0;
	print "$curseq: ";
	my @seqary = split // , $curseq;	#Turn sequence into an array

PATT:	foreach my $patidx (0..$#patterns) {	#loops through pattern styles
		my @pattern = sort by_num @{ $patterns[$patidx] }; #Sorts the indices in @pattern from low to high for regex efficiencies
		next PATT if ($pattern[-1] > $#seqary);	#Skip this pattern if it is longer than the current sequence
		my $expr = gen_regex($curseq,@pattern); #Returns the regex (minus slashes) for the corresponding seq/pattern combo
		unless ($matches{$expr}) { #No need to repeat a regex we've already generated
			@{ $matches{$expr} } = grep /$expr/ , @sequences; #Puts the list of matching sequences in the %matches hash
			$matchcount{$expr} = @{ $matches{$expr} }; #scalar eval of array
			$regexcount++;
			$regexsubt++;
		}			
	}
	print "$regexsubt new regexes\n";
	push @processedseqs,$curseq;
}

my $hr = '-' x 80;

my $sumout = $outpath . $sumfile;
my $sumfh = new IO::File;
print "Writing summary file...\n";

$sumfh->open(">$sumout") or die "Couldn't open $sumout for writing:\n$!";
$sumfh->print("Patterns with $patlen residues:\n");
$sumfh->print("$hr\n\n");

my $output = $outpath . $outfile;
my $outfh = new IO::File;
print "Writing to file...\n";
$outfh->open(">$output") or die "Couldn't open $output for writing:\n$!";
$outfh->print( 	"Sequences: 	 $numseqs\n" . 
		"Positions: 	 $patlen\n" .
		"Patterns: 	 $numpats\n" .
		"Unique Regexes: $regexcount\n" . 
		"$hr\n");
foreach my $expr (sort by_matches keys %matches) { #loop through matched expressions
	next unless ($matchcount{$expr} > $match_thresh);
	$outfh->print( "\nRegex: /$expr/\n$hr\nMatches: $matchcount{$expr}\n$hr\n");
	$sumfh->print( "\/$expr\/\t$matchcount{$expr}\n");
	foreach my $sequence (sort @{ $matches{$expr} }) {
		$outfh->print( "$sequence\n");
	}
}

$outfh->close();
$sumfh->close();
print "Done!\n";

sub by_num { $a <=> $b}

sub by_matches {
	$matchcount{$b} <=> $matchcount{$a};
}

sub gen_regex {
	my $sequence = shift @_;
	my @seqary = split //, $sequence;
	my @pattern = @_;
	my $regex;
	my $placeidx = 0;
	my $lastidx;
	foreach my $idx ($pattern[0]..$pattern[-1]) {
		my $placeholder = $pattern[$placeidx];
		if ($idx == $placeholder) {
			$regex .= $seqary[$idx];
			$placeidx++;
		}
		else {
			$regex .= '.';
		}
	}
	return $regex;
}