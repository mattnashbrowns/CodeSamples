=pod

=head1 Fenrir::Parser -- provides an interface to parse SMARTS data and stores the data in a hash

=cut

package Fenrir::Parser;
use strict;
use IO::File;

use Fenrir::Device;
use Fenrir::Connection;
use Fenrir::Interface;

=over

=item new()
Null constructor creates empty hashes to hold data, sets the input filename to the default
(/usr/local/smarts_data.txt) but this should be changed immediately with the filename() function
and sets up the dispatch table in {CONTROL}

=back
=cut
sub new {
    my $self = {};
    
    $self->{FILENAME} = '/usr/local/smarts_data.txt';
    $self->{FILEHANDLE} = new IO::File;
    $self->{DEVICES} = {};
    $self->{INTERFACES} = {};
    $self->{IPS} = {};
    $self->{CONNECTIONS} = [];
    $self->{CONN_REG} = {};
    $self->{DEV_COUNT} = 0;
    $self->{PORT_COUNT} = 0;
    $self->{CONN_COUNT} = 0;
    #Dispatch table
    $self->{CONTROL} = {
        'hostnames'     =>  \&_parse_hostnames,
        'connections'   =>  \&_parse_connections,
        'interfaces'    =>  \&_parse_ints,
        'ports'         =>  \&_parse_ports,
        'ips'           =>  \&_parse_ips
    };
    bless($self);
    return $self;
}

=over

=item filename() -- gets or sets the location of the SMARTS data file

=back
=cut
sub filename {
    my $self = shift;
    
    if (@_) {
        $self->{FILENAME} = shift;
    }

    return $self->{FILENAME};
}

=over

=item parse() -- Reads input file and maintains a state based on the stanza headers
Stanzas look like # [Keyword]
where [Keyword] is one of Connections, IP Address, Interfaces, Ports
the state established by these stanza headers controls which of the subroutines is called to interpret each line
by invoking the dispatch table stored in $self->{CONTROL}
Makes a first pass through the file to collect all of the device hostnames and port/interface information
Then makes another pass to assemble the connections

=back
=cut
sub parse {
    my $self = shift;
    my $file = $self->{FILENAME};
    my $fh = $self->{FILEHANDLE};
    
    #State control variable
    my $state;

    $fh->open("<$file") or die "Couldn't open $file for reading!\n$!\n";

    #print "First pass...\n";
    #First time through, collect the hostnames and the interfaces
    while (my $line = <$fh>) {
    
        #CRLF conversion
        $line =~ s/\r\n?/\n/g;
        
        #Skip blank lines
        if ($line =~ /^\s*$/) {
            next;
        }
    
    	# Check for the beginning of a Connections stanza
    	if ( $line =~ /^# Connections/ ) {
            $state = 'hostnames';
            #print "Reading hostnames...\n";
            next;
        }
    	
        if ( $line =~ /^# Interfaces/ ) {
            $state = 'interfaces';
            #print "Reading interfaces...\n";
            next;
        }

        if ( $line =~ /^# Ports/ ) {
            #print "Reading ports...\n";
            $state = 'ports';
            next;
        }

        #Check for the beginning of another stanza
        if ($state ne 'skip' && $line =~ /^#/) {
            $state = 'skip';
            next;
        }

        #If we are skipping, and inside a stanza, then skip
        if ($state eq 'skip') {
            next;
        }
    	
    	#Strip the newline
    	chomp $line;
    	
        #Invoke the dispatch table
        $self->{CONTROL}{$state}->($self,$line);
        

    }
	
	#reset to beginning of the file
	$fh->close();
    $fh->open("<$file") or die "Couldn't re-open $file for reading!\n$!\n";
    
    #print "Second pass...\n";
    #Second time through, get all the rest
    while (my $line = <$fh>) {
        
        #Skip blank lines
        if ($line =~ /^\s*$/) {
            next;
        }
        
        if ($line =~ /^# Connections/) {
            $state = 'connections';
            next;
        }

        if ($line =~ /^# IP Address/) {
            $state = 'ips';
            next;
        }

        if ($line =~ /^# Interfaces/) {
            $state = 'skip';
            next;
        }
        
        if ($line =~ /^# Ports/) {
            $state = 'skip';
            next;
        }
        
        #Check for the beginning of another stanza
        if ($state ne 'skip' && $line =~ /^#/) {
            $state = 'skip';
            next;
        }
        
        if ($state eq 'skip') {
            next;
        }

        chomp $line;

        #Invoke dispatch table
        $self->{CONTROL}{$state}->($self,$line);
    }
}

=over

=item _parse_connections($line) -- reads the contents of $line and creates a Fenrir::Connection object to hold
information about the connection that is represented.
Each $line contains zero or more connections

=back
=cut
sub _parse_connections {
    my $self = shift;
    my $line = shift;
    #Split line up into components -- 
    #   $hostname is the name of the device
    #   $conn_string is a space-delimited string containing all of the connection information
    #   $ip is the management IP of the device
    #   $dev_type is one of "ROUTER" or "SWITCH"
    my ($hostname,$conn_string,$ip,$dev_type) = split /;;;/, $line;
    #Split $conn_string up into separate connection statements
    my @tokens = split m/\s/, $conn_string;
    #Loop through the connection statements
    foreach my $conn (@tokens) {
        my $left_int;   #ID of interface on LHS of connection
        my $right_int;  #ID of interface on RHS of connection
        my $left_obj;   #object representing LHS connection
        my $right_obj;  #object representing RHS connection
        my $type;       #the type of connection
        my $ignore = 0; #flag to control whether or not data is stored
        
        #Check to see whether this connection is one we care about,
        #And along the way capture the separate parts
        if ($conn =~ /^(EtherChannel|TrunkCable|Cable|NetworkConnection)::LINK-(\S+)<->(\S+)$/) {
            $type = $1;
            $left_int = $2;
            $right_int = $3;
        } else {
            next;
        }
        
        #Check to see if we know about the LHS interface
        if (!exists($self->{INTERFACES}{$left_int})) {
            #print "In connection $conn\n\tInterface $left_int is not defined!\n";
            $ignore = 1;
        } 
        
        #Check to see if we know about the RHS interface
        if (!exists($self->{INTERFACES}{$right_int})) {
            #print "In connection $conn\n\tInterface $right_int is not defined!\n";
            $ignore = 1;
        }
        
        #Check to see if this is a redundant connection (each connection's reverse is also likely 
        # to be in the file)
        if (
            ((exists($self->{CONN_REG}{$right_int})) && ($self->{CONN_REG}{$right_int} = $left_int))
                                                    ||
            ((exists($self->{CONN_REG}{$left_int}))  && ($self->{CONN_REG}{$left_int} = $right_int))
            ) {
                $ignore = 1;
        }
        
        #Store this connection in the Parser object
        unless ($ignore) {
            my $left_obj = $self->{INTERFACES}{$left_int};
            my $right_obj = $self->{INTERFACES}{$right_int};
            my $conn_obj = Fenrir::Connection->new($left_obj,$right_obj,$type);
            $conn_obj->id($self->{CONN_COUNT}++);
            push @{ $self->{CONNECTIONS} } , $conn_obj;
            $self->{CONN_REG}{$left_int} = $right_int;
        }
    }
    
    
        
}
    


=over

=item _parse_hostnames($line) -- reads the device hostname, management IP, and device type from the Connections stanza(s)
Stores the Fenrir::Device object in the {DEVICES} hash in the Parser object.

=back
=cut
sub _parse_hostnames {
    my ($self,$line) = @_;

    #break up the line into tokens
	my ($hostname,$conn,$ip,$type) = split /;;;/, $line;	
    
    #Make a new Fenrir::Device object
    my $new_device = Fenrir::Device->new();
    #Set all data items on the object
    $new_device->name($hostname);
    $new_device->ip($ip);
    $new_device->type($type);
    $new_device->id($self->{DEV_COUNT}++);
    $self->{DEVICES}{$hostname} = $new_device;
    
    #Store the management IP in the {IPS} hash
    $self->{IPS}{$ip}{HOST} = $hostname;

}


=over

=item _parse_ints($line) -- Reads information about an interface 

=back
=cut
sub _parse_ints {
    my ($self, $line) = @_;
    my @fields = split /;;;/ , $line;
    

    #Read hostname and interface code from first field
    my $int_string = shift @fields;


    #string looks like IF-RTR_RTPMNSC01/1.38
    $int_string =~ /IF-(\S+)\/(\S+)$/;
    my $hostname = $1;
    my $int_id = $2;

    #Get parent Fenrir::Device object
    my $parent_device = $self->{DEVICES}{$hostname};

    #Make sure the device that this interface claims to be part of is actually described in this file
    if (!exists($self->{DEVICES}{$hostname})) {
        #print "Device not defined for Interface $int_string -- skipping\n";
        return;
    }

    #next field is interface name, e.g. Serial1/0
    my $int_name = shift @fields;
    
    #Create Fenrir::Interface object
    my $int_obj = Fenrir::Interface->new($parent_device,$int_id,$int_name,$int_string);

    #There may be extra information on each interface
    #For now, we just care about IP addresses
    foreach my $extra (@fields) {
        if ($extra =~ /IP::IP-(\S+)/) {
            my $ipaddr = $1;
            #Do we need to store in both places?
            $int_obj->ip_addr($ipaddr);
            $self->{IPS}{$ipaddr}{HOST} = $hostname;
        }
    }
 
    #Set the ID for the database
    $int_obj->id($self->{PORT_COUNT}++);
    
    #Attach Interface object to Parser object
    $self->{INTERFACES}{$int_string} = $int_obj;

}

=over

=item _parse_ports($line) -- parses a line from the Ports stanza, which describes a port on a switch

=back
=cut
sub _parse_ports {
    my ($self,$line) = @_;
    my @fields = split /;;;/ , $line;
    
    #String looks like PORT-rmhsbcnes00s03/0.10
    my $port_string = shift @fields;
    
    $port_string =~ /^PORT-(\S+)\/(\S+)/;
    my $hostname = $1;
    my $port_id = $2;
    
    #Check to make sure the device exists
    if (!exists($self->{DEVICES}{$hostname})) {
        #print "Device not found for port $port_string!\n";
        return;
    }
    
    #Get the Fenrir::Device object representing the parent device
    my $parent = $self->{DEVICES}{$hostname};
    
    #Name looks like Fa2/0/4 or some other garbage.  It's the switch's internal name for the port.
    my $port_name = shift @fields;
    
    #Make sure the port has a name; if not, call it 'empty'
    if (!defined($port_name)) {
        $port_name = 'empty';
    }  
    
    #Create a new Fenrir::Interface objet to represent this port
    my $int_obj = Fenrir::Interface->new($parent,$port_id,$port_name,$port_string);

    #Set the ID for the database
    $int_obj->id($self->{PORT_COUNT}++);
    
    #Attach the new Fenrir::Interface object to the Parser object
    $self->{INTERFACES}{$port_string} = $int_obj;
}

=over

=item _parse_ips($line) -- parses a line from the "IP Addresses" section of the file

=back
=cut
sub _parse_ips {
    my ($self,$line) = @_;
    
    #Don't know what the middle field is for
    my ($ip,$ip2,$netmask) = split /;;;/ , $line;
    
    $self->{IPS}{$ip2}{NETMASK} = $netmask;
}



1;