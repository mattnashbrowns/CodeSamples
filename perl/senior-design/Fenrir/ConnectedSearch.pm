package Fenrir::ConnectedSearch;

use strict;
use DBI;

use Fenrir::DB;

use Fenrir::Device;
use Fenrir::Interface;
use Fenrir::Connection;

use Fenrir::Schema;

sub new {
    my $class = shift;
    my $dbname = shift;
    
    my $self = {};
    $self->{'OPEN'} = [];
    $self->{'CLOSED'} = [];
    $self->{RESULTS} = {};
    $self->{CURRENT_LEVEL} = 1;
    
    my $dbo = Fenrir::DB->new;
    $dbo->db_connect($dbname) or die "Failed to connect to database $dbname!\n$!\n";
    
    $self->{SCHEMA} = $dbo->schema;
    
    bless($self);
    return $self;
}


#Same as search, except we get back a reference to a flat structure of arrays --
#One array of hosts (nodes),
#and one array of connections (edges)
sub flat_search {
    my $self = shift;
    my $central_host = shift;
    my $hops = shift;
    
    my $schema = $self->{SCHEMA};
    
    my @unseen;
    my %seen;
    my %seen_connections;
    
    #put central host onto unseen
    push @unseen, {
        hostname        =>      $central_host,
        depth       =>      0
    };
    
    $self->{RESULTS} = {};
    $self->{RESULTS}{RootDevice} = $central_host;
    $self->{RESULTS}{Devices} = [];
    $self->{RESULTS}{Connections} = [];
    
    my $device_list = $self->{RESULTS}{Devices};
    my $conn_list = $self->{RESULTS}{Connections};
    
    

    #Keep pulling host information off the unseen list as long as it exists
    while (@unseen) {
        my $host = shift @unseen;
        my $hostname = $host->{hostname};
        my $depth = $host->{depth};
        
        #Skip this host if we have already seen it
        next if (exists($seen{$hostname}) == 1);
        
        #Mark central host "examined"
        $seen{$hostname} = 1;
        
        
        #Get current host DB row object	    
    	my $host_row = $schema->resultset('Devices')->search({HostName => $hostname})->single;
    	
    	unless (defined($host_row)) {
    	    die "Unknown host $hostname!\n";
    	}
    
        my $this_device = new Fenrir::Device;
        $this_device->name($hostname);
        $this_device->type($host_row->devicetype);
        $this_device->ip($host_row->ipaddr);
        $this_device->netmask($host_row->netmask);
    
        push @$device_list, $this_device;
    	
        #Get list of ports belonging to host
    	my @ports_to_search = $host_row->ports;
    	    
PORT:   foreach my $port_row (@ports_to_search) {
    	
    	    #Get port ID from result row    	    
    		my $port_ID = $port_row->get_column('PortID');
    		my $other_port_ID;
    		
    		#Get any connection in which this port is involved
    		# (Any reason it would be more than 1?)
    		my $conn_row = $schema->resultset('Connections')->search([ {Port1ID => $port_ID}, {Port2ID =>$port_ID} ])->single;
    		
    		next PORT unless ($conn_row);
    		
    		my $conn_id = $conn_row->connection;
    		
    		#Avoid double (or worse) edges
    		next PORT if (exists($seen_connections{$conn_id}));
    		$seen_connections{$conn_id} = 1;
    		
		    my $this_port = Fenrir::Interface->new(
		                                            $this_device,
		                                            $port_row->name,
		                                            $port_row->descrip,
		                                            $port_row->string
		                                            );
		                                            
		    if ($conn_row->get_column('Port1ID') == $port_ID) {
		        $other_port_ID = $conn_row->get_column('Port2ID');
		    } else {
		        $other_port_ID = $conn_row->get_column('Port1ID');
		    }
		    
		    #Get other-port row object from the DB
		    my $other_port_row = $schema->resultset('Ports')->search({PortID => $other_port_ID})->single;
		    
		    #It's relational!
		    my $other_host = $other_port_row->device;
		    my $other_hostname = $other_host->hostname;
		    
		    my $other_device = new Fenrir::Device;
		    $other_device->name($other_hostname);
		    $other_device->type($other_host->devicetype);
		    $other_device->ip($other_host->ipaddr);
		    $other_device->netmask($other_host->netmask);
		    
		    my $other_port = Fenrir::Interface->new(
		                                            $other_device,
		                                            $other_port_row->name,
		                                            $other_port_row->descrip,
		                                            $other_port_row->string
		                                            );
		    
		    my $connection = Fenrir::Connection->new(
		                                            $this_port,
		                                            $other_port,
		                                            $conn_row->conntype
		                                            );
		    
		    #Add the connection to the list, whether we have already seen the host on the other end or not
		    push @$conn_list, $connection;
		    
		    #Is this a new host? 
		    unless (exists($seen{$other_hostname}))    {
		        if  ($depth < ($hops-1) )    { #Have we gone too deep?	        
		            #Then push this host onto the list of hosts to be examined
			        push @unseen,
			            {
			                hostname    =>  $other_hostname,
			                depth       =>  ($depth + 1)
			            };
		        } else { #We are at the max depth and won't be expanding this host
		            push @$device_list, $other_device;
		        }   #Depth check
		    } #Device already seen check
    	} #Port row loop
	} #Hosts while loop 
	
	return $self->{RESULTS};
	
    
}

1;