#!/usr/bin/perl

use strict;
use Cwd;
use File::Spec;
use IO::File;
use Bio::Seq;
use Bio::PrimarySeq;
use Bio::SeqIO;
use Bio::Tools::Run::StandAloneBlast;
use Error qw(:try);
use DateTime;
use Spreadsheet::WriteExcel;

#******************************************************************************
#
#	Global variables and BLAST parameters are all set here
#
#******************************************************************************

$ENV{BLASTDB} = '/usr/bioapps/blast/data';
$ENV{BLASTDIR} = '/usr/bioapps/blast/bin';
my $MIN_PROTEIN_LENGTH = 15;
my $EXCEL_FILENAME = "blast_results.xls";


#Set up BLAST parameters for blast object
my @blast_params = (
	-program		=>	'blastp',
	-database		=>	'nr',
	-outfile		=>	'blast.out'		#We are going to change this later
	);
	
#Create BLAST object
my $blast_factory = Bio::Tools::Run::StandAloneBlast->new(@blast_params);
	
#Trying to match blast settings
$blast_factory->F('F');			#Don't filter query sequence
$blast_factory->v(10);			#"Number of DB sequences to show one-line descriptions for"
$blast_factory->b(10);			#"Number of DB sequences to show alignments for" -- default is 250
$blast_factory->m(7);			#output file format (7 = BLASTXML)
$blast_factory->e(1);			#expect/significance value maximum (default is 10)

#Create aggregated Fasta file to contain all DNA sequences
my $seqs_nt_output = Bio::SeqIO->new(
		-format		=> 	'Fasta',
		-file		=>	">all_nt_seq.fas",
		-alphabet	=>	"dna"
		);

#Create aggregated Fasta file to contain all protein sequences
my $seqs_pro_output = Bio::SeqIO->new(
		-format		=>	'Fasta',
		-file		=>	">all_pro_seq.fas",
		-alphabet	=>	"protein"
		);


# Set up a usage/info message
my $usage = "Usage: newblast.pl -- execute while in the directory containing your .seq files.\n";
$usage .= "Output: \n\t(1)all_nt_seq.fas -- a FASTA file containing all of your NT sequences\n";
$usage .= "\t(2)all_pro_seq.fas -- a FASTA file containing all of your translated peptide sequences\n";
$usage .= "\t(3)<sequence_id>.blast -- a BLAST report for each translated protein\n";


###############################################################################
#	Set up data structures
###############################################################################


my %dna_info;	#Giant hash to hold information about DNA sequences
my %protein_info;	#Giant hash to hold information about protein sequences
my @seqs_to_blast;	#list of non-redundant, long-enough Bio::Seq objects
my %unique_seqs;	#hash of unique protein sequences -- 
					# key: sequence string; value: ID of original sequence
my %blast_results;	#hash of BLAST results -- 
					# key: sequence ID; value: Bio::SearchIO object
					# (see http://bioperl.open-bio.org/wiki/HOWTO:SearchIO)

#Options to pass to the Bio::Seq translate() method
my %translate_options = (
	-complete	=>	1, #expect a complete DNA sequence (contains start and stop codons)
	-orf		=>	1	#start translating from the first open reference frame
);

my @seqfiles = <*.seq>;		#List of all sequence files in the current directory

#de-buffer STDOUT
$|++;

if ((scalar @seqfiles) == 0) {
	print "Couldn't find any sequence files in this directory!\n";
	die $usage;
}


###############################################################################
#	Getting down to business
###############################################################################

print "Reading sequence files...\n";

foreach my $seqfile (@seqfiles) {
	print "\t$seqfile\n";
	#extract the filename from the path
	my ($junk, $pathname, $filename) = File::Spec->splitpath($seqfile);
	
	#make an ID out of the filename
	my $id = $filename;
	$id =~ s/\.seq//;
	
	my $seqfh = IO::File->new();
	$seqfh->open("<$seqfile") or die "Couldn't open sequence file $seqfile:\n$!\n";
	
	my $seqtext;	#contains the actual text of the NT sequence
	
	# Read the plain text .seq file line by line, assembling the sequence
	# and eating newlines
	while (my $seqline = <$seqfh>)  {
		#This takes out the CR inserted by the PC world
		$seqline =~ s/\cM//g;
		chomp $seqline;
		$seqtext .= $seqline;
	}
	
	#Be polite
	$seqfh->close();
	
	#Make a Bio::Seq object out of the NT sequence
	my $ntSeq = Bio::Seq->new(
		-seq	=>		$seqtext,
		-id		=>		$id
	);
	
	
	#Write the new sequence to the aggregated NT FASTA file
	$seqs_nt_output->write_seq($ntSeq);
	
}

# We're done with this object
undef $seqs_nt_output;

# create a new object referring to the file holding all the DNA sequences
#	to read from
my $seqs_nt_input = Bio::SeqIO->new(
	-format		=> 	'Fasta',
	-file		=>	"all_nt_seq.fas",
	-alphabet	=>	"dna"
	);

print "Translating DNA sequences...\n";

#Now loop through all of the DNA sequences we just wrote out
while (my $ntSeq = $seqs_nt_input->next_seq()) {
	my $seq_id = $ntSeq->display_id();
	
	print "\t$seq_id: ";
	
	# trim_dna returns a hashref that we stick into the dna_info hash
	$dna_info{$seq_id} = trim_dna($ntSeq);
	
	# if trim_dna can't find an appropriate start site, it sets "start" to "X"
	if ($dna_info{$seq_id}->{"start"} eq 'X') {
		print "no start site\n";
		$protein_info{$seq_id}{'status'} = 'No start site found';
		next;
	} 
	
	#Translate the trimmed sequence into protein
	my $trimmed_obj = $dna_info{$seq_id}->{core};
	my $translated = $trimmed_obj->translate(%translate_options);	
	$seqs_pro_output->write_seq($translated);
	$protein_info{$seq_id}{'sequence'} = $translated->seq();
	print $translated->seq() . "\n";
	
}

# We're done with output, so free up resources
undef $seqs_pro_output;

my $seqs_pro_input = Bio::SeqIO->new(
		-format		=>	'Fasta',
		-file		=>	"all_pro_seq.fas",
		-alphabet	=>	"protein"
		);

#Remove duplicate sequences (exactly identical protein sequences)
#And sequences that are too short (min length defined at the top of the script)
print "Weeding out junk...\n";
while (my $proSeq = $seqs_pro_input->next_seq()) {
	my $this_id = $proSeq->id();
	my $seq_string = $proSeq->seq();
	
	if ($proSeq->length() < $MIN_PROTEIN_LENGTH) {
		print "$this_id too short\n";
		$protein_info{$this_id}{'status'} = "Protein sequence too short";
		next;
	}

	#Check to see if we have already seen this protein sequence
	if (exists $unique_seqs{$seq_string}) {
		my $original_id = $unique_seqs{$seq_string};
		print "$this_id is duplicate of $original_id \n";
		$protein_info{$this_id}{'status'} = "Duplicate of $original_id";
		next;
	} else { #If we haven't, make sure to make a note of it
		$unique_seqs{$seq_string} = $this_id;
	}
	
	push @seqs_to_blast, $proSeq;
}


print "\nRunning BLAST against proteins...\n";

# run through non-redundant protein sequences and BLAST them
foreach my $uniqueSeq (@seqs_to_blast) {
	my $this_id = $uniqueSeq->id();
	print $this_id . "\n";
	blast_it($uniqueSeq,$blast_factory);
}

my @blastfiles = <*.blast>; #List of all BLAST report files in the current directory

print "Parsing BLAST reports...\n";

if ( (scalar @blastfiles) == 0) {
	print "No BLAST reports were generated!\n";
}

foreach my $blastfile (@blastfiles) {
	my ($junk, $pathname, $filename) = File::Spec->splitpath($blastfile);
	
	#extract ID from filename
	my $id = $filename;
	$id =~ s/\.blast//;
	print "\t$id\n";
	my $blast_input = new Bio::SearchIO(
											-format		=>	'blastxml',
											-file		=>	$blastfile,
											-tempfile	=> 	1			#use a temp file
										);
	
	#Each report can have multiple results
	while (my $result = $blast_input->next_result() ) {
		#And each result can have multiple hits
		while (my $hit = $result->next_hit()) {
			my $desc = $hit->description;
			#Skip this hit unless it belongs to an interesting organism
			next unless ($desc =~ /(Homo sapiens)|(Mus musculus)|(Rattus norvegicus)|(Bos taurus)/);
			
			push @{ $protein_info{$id}{'hits'} }, $hit;
			print "\t\t$desc\n";
		}
	}
	
}

print "Excel setup...\n";

my $workbook 	= Spreadsheet::WriteExcel->new($EXCEL_FILENAME);
my $results_ws 	= $workbook->addworksheet("BLAST results");
#my $seqs_ws		= $workbook->addworksheet("Sequence detail");


populate_results_ws($results_ws, \%protein_info);
#populate_seq_ws($seqs_ws,\%protein_info);



print "\nDone!\n";




# trim_dna takes a Bio::Seq object as its only argument
# looks for an appropriate start site,
# and trims the front of sequence if it finds one.
# The start site and the trimmed sequence are put into a hash:
# %info_hash = (
#	start	=>	start_site (text),
#	core	=>	trimmed_seq (Bio::Seq object)
#	raw		=>	original seq (Bio::Seq object)   ***DO WE NEED THIS?
# a reference to this hash is returned.
# if a start site can't be found, "start" is set to "X"
sub trim_dna {
	my $raw_seq = shift; #Bio::Seq object passed as argument
	my $seq_string = $raw_seq->seq(); #The untrimmed DNA sequence
	my $EcoRI = "GAATTC"; #EcoRI start site
	my $BamHI = "GGATCC"; #BamHI start site
	my $start_pos; #index of the starting position
	my %info_hash; #holds start, end, and core information
	my $start_pos;
	
	my $seq_length = $raw_seq->length();
	
	$start_pos = index($seq_string,$EcoRI);
	
	if ($start_pos == -1) { #We couldn't find EcoRI, looking for BamHI
		$start_pos = index($seq_string,$BamHI);
	} else { #start site is EcoRI
		$info_hash{"start"} = $EcoRI;
	}
	
	if ($start_pos == -1) { #We STILL couldn't find a start site!  So we give up.
	  %info_hash = (
	  	start	=>	"X",
	  	raw		=>	$raw_seq
	  );
	  return \%info_hash;
	}
	
	unless (exists $info_hash{"start"}) {
		$info_hash{"start"} = $BamHI;
	}
	
	
	
	# get the section of DNA that we want to translate, as a Bio::Seq object
	my $core = Bio::PrimarySeq->new(
					-seq	=>	$raw_seq->subseq($start_pos+2,$seq_length),
					-id		=>	$raw_seq->id
					);
	# The reason for +2:
	# subseq method was clearly written by a non-engineer,
	# who used a 1-based character array
	# while index() is 0-based like every other damn thing
	# AND we want to start just after the first nt in the start site
	
	$info_hash{"core"} = $core;
	$info_hash{"raw"} = $raw_seq;
	
	return \%info_hash;
	
}

# performs a blast against the sequence object passed as the first argument.
# Any kind of blast can be performed against any kind of sequence object -- just set the parameters of 
# $blast_obj before you pass it in.
sub blast_it {
	my $seq_obj = shift;
	my $blast_obj = shift;
	my $blast_report;
	
	my $seqlen = $seq_obj->length();
	my $seq_id = $seq_obj->id();
	
	my $blastfile = $seq_id . '.blast';
	$blast_obj->outfile($blastfile);
	
	my $start_time = DateTime->now();
	
	try {
		$blast_report = $blast_obj->blastall($seq_obj);
	} catch Error with {
		my $error = shift;
		print "\nException caught when BLASTing sequence " . $seq_obj->display_id() . "\n";
		print $error->{-text};
		return undef;
	};
	
	my $finish_time = DateTime->now();
	
	my $elapsed = $finish_time - $start_time;
	
	print "Elapsed time: " . $elapsed->in_units('minutes') . " minutes\n";
}

#Fills out the Excel worksheet with BLAST results
sub populate_results_ws {
	my $ws = shift;
	my $prots = shift;
	my $row = 0;
	
	
	my @header = ("SEQ ID","Hit ID","Hit Description","Score","E-Value");
	$ws->write($row++,0,\@header);
	
	foreach my $seq_id (sort keys %$prots) {
		if (exists $prots->{$seq_id}{'status'}) {
			my @statusrow = ($seq_id,"",$prots->{$seq_id}{'status'},"","");
			$ws->write($row++,0,\@statusrow);
			next;
		}
		
		foreach my $hit_obj (@{ $prots->{$seq_id}{'hits'} }) {
			my @result_row = (	
								$seq_id,
								$hit_obj->name,
								$hit_obj->description,
								$hit_obj->score,
								$hit_obj->significance
							);
			$ws->write($row++,0,\@result_row);
		}
		
	}
}
