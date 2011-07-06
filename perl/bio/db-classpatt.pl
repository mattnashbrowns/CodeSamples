# db-classpatt.pl
# Version 0.9a by Matt Nash 28 August 2005
# mattnash@intrex.net

# Generates huge output files and consumes all of your memory
# But it does so with great efficiency
# Also dumps lots of junk to the screen
# But what does it do?
# It reads in a file of sequences, one per line
# And creates a (largish) number of regular expressions based on the
# patlen argument. For a sequence of length n and a patlen k, the number
# of regular expressions is n!/(k!*(n-k)!)
# This is accomplished through the Math::Combinatorics module

# After that, the amino acid alphabet that is defined below in %tbmap
# is used to create more general regular expressions, which I call
# "classexes" throughout the script.
# This uses the Set::CrossProduct module and its numbers are truly
# staggering.  You will get a sense of just how staggering if you monitor
# the screen output.
# I would love to make it prettier (the screen output) but you will want
# to know if it freezes, and what is happening when it does
# For example, if you have a sequence that contains non-amino characters,
# You will be sad.
# In the output, the line that begins '*-' contains the number of classes
# that the current fixed regex can translate to, one per position.
# The next line is the cardinality of the cross product that will be performed
# If any of these numbers is zero, you will be sad.
# If you do not have lots of disk space, you will be sad.
# If you have sequences that are significantly longer than 20, you will
# be VERY sad.

# generated classcodes of the form /l.....a...w/ will be written
# to a SQLite database along with the number of times they matched.
# They will only be committed after every 10,000 classcodes,
# and at the end of the script.
# It will be named something like class-matches-n.db3 
# Where 'n' is the pattern length you have specified.
# More sophisticated database structure and output is planned
# for The Future.
# In the future, everything will work. (TM)


# Free for all uses
# Free to modify -- just include this notice
# Syntax: classpatt.pl [patlen] [match_thresh] [input filename] [output file prefix]
#
#
# patlen: number of fixed positions to use in generated patterns
# match_thresh: number of matches required before we are interested in a particular generated regex
# [input filename]: A file containing your sequences of any type, one per line
# [output file prefix] -- a number indicating the number of residues in the pattern
# will be appended, along with a ".db3" file extension, to the value here


use strict;
use IO::File;
use Math::Combinatorics;
use Set::CrossProduct;
use DBI;
use DBD::SQLite;
#use Memoize;

#memoize('get_classes');

#Change default values here
my $patlen = 3;  #The number of residues in our patterns
my $match_thresh = 10;	#The number of matches required before we include it in our output file
my $infile = "large-dataset.txt"; #The input file
my $outfile = "class-matches"; #The output file
$|++; #buffer flushing - "unbuffer STDOUT"

#Change input and output paths here
my $inpath = "C:\\matt\\perl\\ryan\\";
my $outpath = $inpath;



if (!(@ARGV)) {
	print 	"Using default values:\n" .
		"    Positions: $patlen\n" .
		" Min. matches:	$match_thresh\n" .
		"   Input file:	$infile\n" .
		"  Output file:	$outfile-$patlen\n";
	sleep 3;
} else {
	$patlen = shift @ARGV;
	$match_thresh = shift @ARGV if (@ARGV);
	$infile = shift @ARGV if (@ARGV);
	$outfile = shift @ARGV if (@ARGV);
}

$outfile .= "-$patlen.db3";

my $dbh = DBI->connect("dbi:SQLite:$outfile","","",
			{AutoCommit => 0 } ) 
		or die "Couldn't open db file $outfile:\n$!";

#Later we are going to see if the tables already exist;
#For now we are assuming the file is new each time.

#Create tables
db_prepare($dbh);


#Set up your assignments of amino acids to groups here.
#They will be easier to read if you alpha-sort each group's list
#Note that we have not always bothered to do this.

my $alcohols 	= 	'ST';
my $aliphatic 	= 	'GAVLIP';
my $amides 	= 	'NQ';
my $aromatic 	= 	'FYW';
my $charged	=	'DEHKR';
my $hydrophobic	=	'ACFGHIKLMRTVWY';
my $hydroxyl	=	'STY';
my $negative	= 	'DE';
my $polar	=	'CDEHKNQRST';
my $polar_neut	=	'STNQ';
my $positive	=	'HKR';
my $small	=	'ACDGNPSTV'; 
my $sulfur	=	'CM';
my $tiny	=	'AGS';
my $turnlike	=	'ACDEGHKNQRST';

#Here you set up the particular code you want to use for each group
#It doesn't really matter what it is as long as it's lower case
#I guess you could use one of the unused capital letters of the alphabet
#But I wouldn't want to follow behind you picking up the shattered remains
#Of your code.
my %tbmap = (
	'p' => $aliphatic,
	'r' => $aromatic,
	's' => $small,
	'l' => $polar,
	'h' => $charged,
	'y' => $hydroxyl,
	'n' => $negative,
	'u' => $polar_neut,
	't' => $positive,
	'f' => $sulfur,
	'k' => $turnlike,
	'w' => $tiny,
	'c' => $alcohols,
	'd' => $amides,
	'o' => $hydrophobic,
	A => 'A', C => 'C', D => 'D', E => 'E', F => 'F', 
	G => 'G', H=> 'H', I => 'I', K => 'K', L => 'L',
	M => 'M', N => 'N', P => 'P', Q => 'Q', R => 'R', 
	S => 'S', T => 'T', V => 'V', W => 'W', Y => 'Y'
	);

my %tbreverse;

#Create the reverse-lookup hash based on what is configured above
foreach my $classcode (keys %tbmap) {
	my @classary = split // , $tbmap{$classcode};
	foreach my $classmembr (@classary) {
		push @{ $tbreverse{$classmembr} } , $classcode;
	}
}

my $infh = new IO::File;
my $input = $inpath . $infile;
$infh->open("<$input") or die "Couldn't open $input for reading\n";

my @sequences;
my $maxlen=0;

#Start a transaction, but don't commit each time
#$dbh->do("BEGIN DEFERRED");

print "Reading input sequences\n";
LINE: while (my $line = <$infh>) {
	chomp $line;
	foreach my $curseq (@sequences) { #Ignore duplicate sequences
		next LINE if ($curseq eq $line);
	}
	push @sequences, $line;
	$dbh->do("INSERT INTO sequences (sequence)
		VALUES ('$line')");
	my $linelen = length $line;
	$maxlen = $linelen unless ($maxlen > $linelen);
	print ".";
}

$dbh->commit();

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

my $classexcount=0;
my $seqcount = 0;
my %regex_reg;
my @classcode_reg;
my $insertctr = 0;

#my $output = $outpath . $outfile;
#my $outfh = new IO::File;
#$outfh->open(">$output") or die "Couldn't open output file $output:\n$!";


my $clx_sql = "INSERT INTO classexes (classex , match_ct)
		VALUES (? , ?)";
my $clx_sth = $dbh->prepare($clx_sql);
		

print "Processing sequences\n";
SEQ: foreach my $curseq (@sequences) { #loop through sequences
	print "$curseq\n";
	#sleep 1;
	my @seqary = split // , $curseq;	#Turn sequence into an array
	$seqcount++;
PATT:	foreach my $patidx (0..$#patterns) {	#loops through pattern styles
		my @pattern = sort by_num @{ $patterns[$patidx] }; #Sorts the indices in @pattern from low to high for regex efficiencies
		next PATT if ($pattern[-1] > $#seqary);	#Skip this pattern if it is longer than the current sequence
		my $expr = gen_regex($curseq,@pattern); #Returns the regex (minus slashes) for the corresponding seq/pattern combo
		next PATT if ($regex_reg{$expr});
		$regex_reg{$expr} = 1;
		print "\t$expr\tSequence $seqcount\n";
		print "*";
		my $classexes = gen_classex($expr);
		print "#\n";
		my $patternmatches = 0;
		my $classexsubt = 0;
		
		
CLASSCODE:	foreach my $classcode (keys %$classexes) {
			my @matches;
			my $matchctr;
			
			my $classex = $$classexes{$classcode};
			@matches = grep /$classex/ , @sequences;
			$matchctr = scalar @matches;
			
			if ($matchctr > $match_thresh) {
				$clx_sth->execute($classcode , $matchctr); 
				$insertctr++;
			}
			
			if ($insertctr > 10000) {
				print "Committing...\n";
				$dbh->commit();
				$insertctr = 0;
			}
			
			$patternmatches += $matchctr;
			$classexcount++;
			$classexsubt++;
			
		}
		
		print "\n$classexsubt new classexes\t matched $patternmatches times\n";
		undef $classexes;
	}
	
}


my $hr = '-' x 80;

$dbh->commit;
$clx_sth->finish;
$dbh->disconnect();

print "Done!\n";

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


#gen_classex ($): When passed a regex generated by gen_regex,
#returns a list of more general regexes making use of the classes
#of amino acids defined at the top of the script
sub gen_classex {
	my $this_regex = shift;		#Puts the arg in $this_regex
	my @reg_ary = split // , $this_regex;	#Turns regex into array
	my @classes;			#AoA of class lists, each A corresponding to a single residue
	my %classexes;			#List of new regexes
	undef %classexes;
	print "-";
	my $aminos;
	foreach my $idx (0..$#reg_ary) {	#Loops through each char in regex
		next if ($reg_ary[$idx] eq '.');#Skips char if it is a wildcard
		$aminos .= $reg_ary[$idx];
	}
	print "=";
	@classes = get_classes($aminos); #Makes AoA for cross product
	print "-\n";
	
	#Create a new Set::C-P object which will iterate through all
	#possible combinations of class codes
	#See the docs on Set::CrossProduct for more info
	my $iterator = Set::CrossProduct->new( \@classes );
	my $card = $iterator->cardinality();
	print "$card ";
	#get() function returns the next combination of bucket contents
	while ( my $cur_tuple = $iterator->get() )	{
		my $classex;
		my $classcode;	
		#print "p";
		foreach my $reg_idx (0..$#reg_ary) {
			if ($reg_ary[$reg_idx] eq '.') {
				$classex .= '.';
				$classcode .= '.';
			}
			else {
				my $class = shift @$cur_tuple;
				$classex .= '[' . $tbmap{$class} . ']';
				$classcode .= $class;
			}
		}
		$classexes{$classcode} = $classex;
	}
	undef $iterator;
	undef @classes;
	return \%classexes;
}	

sub by_num {
	$a <=> $b;
}

sub db_prepare {
	my $dbhandle = shift;
	my $seqtbl = "CREATE TABLE sequences (
		seqid			INTEGER PRIMARY KEY,
		sequence		TEXT)";
	my $clasxtbl = "CREATE TABLE classexes (
		clxid			INTEGER PRIMARY KEY,
		classex			TEXT,
		match_ct		INTEGER)";
	my $matchtbl = "CREATE TABLE matches (
		matchid			INTEGER PRIMARY KEY,
		clxid			INTEGER,
		seqid			INTEGER)";
	$dbhandle->do($seqtbl);
	$dbhandle->do($clasxtbl);
	
	#Not ready to implement this yet
	#$dbhandle->do($matchtbl);
}

sub get_classes {
	my $aminos = shift;
	my @ami_list = split // , $aminos;
	my @classlist;
	foreach my $ami (@ami_list) {
		push @classlist , \@{ $tbreverse{$ami} };
	}
	return @classlist;
}