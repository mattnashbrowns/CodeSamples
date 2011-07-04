package Fenrir::DB;

use DBI;
use Fenrir::Schema;
use strict;
use Net::CIDR;


sub new {
    my $self = {};
    $self->{HOST} = 'localhost';
    $self->{PORT} = 3306;
    $self->{DBUSER} = 'fenrir';
    $self->{DBPASS} = 'tuesdays!dead';
    bless($self);
    return($self);
}

#Initialize the database --
#Drop it, then re-create it
sub db_init {
    my $self = shift;
    my $dbname = shift;
    my $host = $self->{HOST};
    my $port = $self->{PORT};
    my $user = $self->{DBUSER};
    my $pass = $self->{DBPASS};
    
    #Assemble connection string
    my $dsn = "DBI:mysql:database=$dbname;host=$host;port=$port";
    #Get driver handle 
    my $drh = DBI->install_driver("mysql");
    
    #delete and create db
    $drh->func('dropdb', $dbname, $host, $user, $pass, 'admin');
    $drh->func('createdb',$dbname, $host, $user, $pass, 'admin');
    
    #Load up Fenrir DB objects
    Fenrir::Schema->load_classes();
    
    #Connect to the DB with DBIx::Class Schema
    my $schema = Fenrir::Schema->connect($dsn,$user,$pass);
    
    #Create tables as defined in DBIx::Class objects
    $schema->deploy();
    
    $self->{SCHEMA} = $schema;
    $self->{DBNAME} = $dbname;
}

sub schema {
    my $self = shift;
    return $self->{SCHEMA};
}

#connect to the db and get a schema object
sub db_connect {
    my $self = shift;
    my $dbname = $self->{DBNAME} || shift;
    
    my $host = $self->{HOST};
    my $port = $self->{PORT};
    my $user = $self->{DBUSER};
    my $pass = $self->{DBPASS};
    
    #Assemble connection string
    my $dsn = "DBI:mysql:database=$dbname;host=$host;port=$port";
    
    #Connect to the db    
    my $schema = Fenrir::Schema->connect($dsn,$user,$pass);

    $self->{SCHEMA} = $schema;
    $self->{DSN} = $dsn;
    
    return $schema;
}

sub write_all_data {
    my $self = shift;
    #Fenrir::Parser object containing all SMARTS data to be written
    my $po = shift;
    
    my $schema = $self->{SCHEMA};
    
    my @dev_data;
    my @port_data;
    my @conn_data;
    
    #Process host data
    #print "Reading devices...";
    foreach my $hostid (keys %{ $po->{DEVICES} }) {
        my $type = $po->{DEVICES}{$hostid}->type();
        my $devid = $po->{DEVICES}{$hostid}->id();
        my $ipaddr = $po->{DEVICES}{$hostid}->ip();
        my $netmask = $po->{IPS}{$ipaddr}{NETMASK};
        ##print '*';
        push @dev_data, [$devid,$hostid,$type,$ipaddr,$netmask];
    }
    
    #print "\nWriting...";
    my $dev_rows = $schema->populate('Devices', [
        [qw/DevID HostName DeviceType IPAddress Netmask/],
        @dev_data,
    ]);
    ##print "Done\n";
    
    #Process port/interface data
    #print "Reading ports...";
    foreach my $int_string (keys %{ $po->{INTERFACES} }) {
        my $int_obj = $po->{INTERFACES}{$int_string};
        my $id = $int_obj->id();
        my $name = $int_obj->name();
        my $desc = $int_obj->desc();
        my $ip_addr = $int_obj->ip_addr();
        my $dev_id = $int_obj->device()->id();
        ##print '*';
        push @port_data, [$id,$name,$desc,$int_string,$dev_id,$ip_addr];
    }
    
    #print "\nWriting...";
    my $port_rows = $schema->populate('Ports', [
        [qw/PortID PortName PortDescription PortString DevID IPAddress/],
        @port_data
    ]);
    #print "Done\n";
    
    #Process connection data
    #print "Reading connections...";
    foreach my $conn_obj (@{ $po->{CONNECTIONS} }) {
    
        my $conn_id = $conn_obj->id();
        my $ints = $conn_obj->interfaces();
        my ($int1,$int2) = @$ints;
        
        if ( !defined($int1) || !defined($int2) ) {
            die "An interface was not defined for connection $conn_id\n";
        }
        
        my $int1_id = $int1->id();
        
        my $int2_id = $int2->id();
        
        my $type = $conn_obj->type();
        ##print '*';
        push @conn_data, [$conn_id,$type,$int1_id,$int2_id];
    }
    
    #print "\nWriting...";
    my $conn_rows = $schema->populate('Connections', [
        [qw/ConnID ConnectionType Port1ID Port2ID/],
        @conn_data
    ]);
    #print "Done\n";
}

sub get_all_hosts {
    my $self = shift;
    my $schema = $self->{SCHEMA};
    
    my @hostlist = $schema->resultset('Devices')->all;
    return \@hostlist;
}

sub db_list {
    my $self = shift;
    
    my $host = $self->{HOST};
    my $port = $self->{PORT};
    my $user = $self->{DBUSER};
    my $pass = $self->{DBPASS};
    
    
    my @dbstrings = DBI->data_sources("mysql",
      {"host" => $host, "port" => $port, "user" => $user, password => $pass});
    
    my @databases;
    
    foreach my $string (@dbstrings) {
        $string =~ s/DBI:mysql://g;
        next if ($string eq 'mysql' or $string eq 'information_schema');
        push @databases, $string;
    }
    
    return \@databases;
}

1;
