use strict;

package Fenrir::WebApp;

use base qw/CGI::Application/;

use CGI::Application::Plugin::AutoRunmode;
use Fenrir::DB;
use Fenrir::Parser;
use Fenrir::ConnectedSearch;
use Fenrir::Graph;
use XML::Simple;
use Data::Dumper;
use Graph::Easy::Parser::Graphviz;

#Safe for hostnames, etc
my $SAFE_CHARS = 'a-zA-Z0-9-._';
#Safe for MySQL identifiers
my $DB_CHARS = 'a-zA-Z0-9_';

sub setup {
    $ENV{SERVER_NAME} = 'localhost';
    $ENV{GV_FILE_PATH} = '/var/www/html/images/';
}

#initialize DB
sub db_init :Runmode {
    my $self = shift;
    my $q = $self->query();
    
    my $dbname = $q->param('dbname');
    
    $dbname =~ s/[^$DB_CHARS]/_/g;
    
    if ( ($dbname =~ /[A-Za-z]/) && ($dbname =~ /^([$DB_CHARS]+)$/) ){
        $dbname = $1;
    } else {
        die "Invalid characters in DB name!\n";
    }
    
    my $dbo = new Fenrir::DB;
    $dbo->db_init($dbname);
}


#Parse file and write to DB
sub do_parse :Runmode {
    my $self = shift;
    my $q = $self->query();
    my $po = Fenrir::Parser->new();
    my $dbo = Fenrir::DB->new();
    
    my $input_path = '/fenrir/uploads/';
    
    $self->header_add( -type    =>  'text/xml' );
    my %output_hash;
    my $output;
    my $xs = new XML::Simple;
    
    my $file = $q->param('filename');
    my $dbname = $q->param('dbname');    
    
    $file =~ tr/ /_/;
    $file =~ s/[^$SAFE_CHARS]//g;
    
    if ($file =~ /^([$SAFE_CHARS]+)$/) {
        $file = $1;
    } else {
        die "Illegal characters in filename!\n";
    }
    
    $dbname =~ s/[^$DB_CHARS]/_/g;
    
    if ($dbname =~ /^([$DB_CHARS]+)$/) {
        $dbname = $1;
    } else {
        die "Illegal characters in db name!\n";
    }
    
    $dbo->db_connect($dbname);
    
    $po->filename("$input_path$file");
    
    $po->parse();
    
    $dbo->write_all_data($po);
    
    my $devlist = $dbo->get_all_hosts;
    
    foreach my $dev (@$devlist) {
        push @{ $output_hash{Data}{Device} },
            {   
                hostname   =>  $dev->get_column('HostName')        
            };
    }
    
    #$output .= $q->header();
    
    
    $output .= '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    #$output .= '<meta http-equiv="Content-type" content="text/html; charset=utf-8"/>' . "\n";
    
    $output .= $xs->XMLout(
        \%output_hash,
        AttrIndent      =>  1,
        NoAttr          =>  1,
        KeepRoot        =>  1
    );
    
    return $output;
}


sub make_graph :Runmode {
    my $self = shift;
    my $q = $self->query();
    
    my $dbname = $q->param('dbname');
    my $hostname = $q->param('hostname');
    my $hops     = $q->param('hops');
    my $type    = $q->param('type');
    my $format  = $q->param('format');
    my $elabels = $q->param('edge_labels');
    
    $elabels = 1 if (defined($elabels) && ($elabels eq 'yes'));
    
    unless ($type) {
        $type = 'fdp';
    }
    
    unless ($format) {
        $format = 'png';
    }
    
    $self->header_add( -type    =>  'image/png' );
    
    
    if ($dbname =~ /^([$DB_CHARS]+)$/) {
        $dbname = $1;
    } else {
        die "Unsafe chars in dbname!\n";
    }
    
    if ($hostname =~ /^([$SAFE_CHARS]+)$/) {
        $hostname = $1;
    } else {
        die "Unsafe chars in hostname!\n";
    }
    
    if ($hops =~ /^([0-9]+)$/) {
        $hops = $1;
    } else {
        die "Invalid value for hops!\n";
    }
    
    if ($type =~ /^([$SAFE_CHARS]+)$/) {
        $type = $1;
    } else {
        die "Invalid characters in type!\n";
    }
        
    my %options = (
    name        =>  $hostname,
    directed    =>  0,
    overlap     =>  'scale',
    layout      =>  $type
    );
        
    my $go = Fenrir::Graph->new($dbname,$hostname,$hops);
    $go->init_graph(\%options);
    $go->get_results;
    
    my $g = $go->populate_results($elabels);
    
    my $output;
    
    if ($format eq 'svg') {
        $self->header_add( -type    =>  'image/svg+xml' );
        $output = $g->as_svg();
    } elsif ($format eq 'dot') {
        $self->header_add( -type    => 'text/plain' );
        $output = $g->as_text();
    } else {
        $output = $g->as_png();
    }
    
    return $output;
    
}

sub db_list :Runmode {
    my $self = shift;
    
    $self->header_add( -type    =>  'text/xml' );
    
    my $dbo = new Fenrir::DB;
    
    my $xs = new XML::Simple;
    
    my $dblist = $dbo->db_list;
    
    my %dbdata;
    
    foreach my $db (@$dblist) {
        push @{ $dbdata{DATA}{Database} }, $db;
    }
    
    my $output;
    
    $output .= '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $output .= $xs->XMLout(
        \%dbdata,
        AttrIndent      =>  1,
        NoAttr          =>  1,
        KeepRoot        =>  1
    );
    
    return $output;
}

sub device_list :Runmode {
    my $self = shift;
    $self->header_add( -type    =>  'text/xml' );
    my $q = $self->query();
    
    my $dbname = $q->param('dbname'); 
    
    my $dbo = new Fenrir::DB;
    my $xs = new XML::Simple;
    my $output;
    
    my %output_hash;
    my $devlist;
    
    $dbname =~ s/[^$DB_CHARS]/_/g;
    
    if ($dbname =~ /^([$DB_CHARS]+)$/) {
        $dbname = $1;
    } else {
        die "Invalid characters in database name!";
    }
    
    $dbo->db_connect($dbname);
    
    $devlist = $dbo->get_all_hosts;
    
    foreach my $dev (@$devlist) {
        push @{ $output_hash{Data}{Device} },
            {   
                hostname   =>  $dev->get_column('HostName')        
            };
    }
    
    $output .= '<?xml version="1.0" encoding="UTF-8"?>' . "\n";
    $output .= $xs->XMLout(
        \%output_hash,
        AttrIndent      =>  1,
        NoAttr          =>  1,
        KeepRoot        =>  1
    );
    
    return $output;
    
}

1;