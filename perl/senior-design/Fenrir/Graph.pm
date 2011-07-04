package Fenrir::Graph;

use strict;
use Fenrir::ConnectedSearch;
use Fenrir::DB;
use GraphViz;

#Takes dbname, root device, #hops as arguments
sub new {
    my $self = {};
    my $class = shift;
    $self->{DBNAME} = shift;
    $self->{ROOT} = shift;
    $self->{HOPS} = shift;
    bless $self;
    return $self;
}

#Creates graph object
#Takes optional hashref of GV options
sub init_graph {
    my $self = shift;
    my $gv;
    
    if (@_) {
        $gv = GraphViz->new(shift);
    } else {
        $gv = GraphViz->new(
            directed        =>  0,
            overlap         =>  'scalexy',
            layout          =>  'fdp',
            outputorder     =>  'edgesfirst'     
        );
    }
    
    $self->{GV} = $gv;
}   

#Performs search on database and pulls results into a hash
#Consisting of an array of Fenrir::Device objects,
#an array of Fenrir::Connection objects,
#and a single entry holding the name of the central host
sub get_results {
    my $self = shift;
    my $dbname = $self->{DBNAME};
    
    my $cs = Fenrir::ConnectedSearch->new($dbname);
    
    my $root_host = $self->{ROOT};
    my $hops = $self->{HOPS};
    
    my $results = $cs->flat_search($root_host,$hops);
    
    $self->{RESULTS} = $results;
}

sub populate_results {
    my $self = shift;
    my $edge_labels = shift;
    my $data = $self->results;
    
    my $g;
    
    if (exists($self->{GV})) {
        $g = $self->{GV}
    } else {
        die "Graph object not initialized!  Use init_graph function first!\n"
    }
    
    my $root_hostname = $data->{RootDevice};
    
    foreach my $device (@{ $data->{Devices} }) {
    
        my $hostname = $device->name;
        my $ipaddr = $device->ip;
        my $netmask = $device->netmask;
        my $dev_type = $device->type;
        
        my $cluster_attrs = {
            'name'          =>      "clust_$hostname",
            'label'         =>      "$hostname\n$ipaddr\n$netmask",
            'labelloc'      =>      "t",
            'style'         =>       "filled",
            'fillcolor'     =>      "white"
        };
    
        my $node_attrs = {
            'name'          =>      $hostname,
            'shape'         =>      'none',
            'cluster'       =>      $cluster_attrs,
            'style'         =>      "invis",
            'label'         =>      ""
        };
    
        if ($dev_type eq 'ROUTER') {
            $node_attrs->{shapefile} = 'http://152.14.85.250/images/router.png';
        } else {
            $node_attrs->{shapefile} = 'http://152.14.85.250/images/switch.png';
        }
    
        #Mark the device that is the root host
        if ($hostname eq $root_hostname) {
            $cluster_attrs->{color} = "red";
            $cluster_attrs->{fontcolor} = "red";
        }
    
        $g->add_node($node_attrs);
    }
    
    foreach my $conn ( @{ $data->{Connections} } ) {
        
        my $ports = $conn->interfaces;
        
        my $port1 = $ports->[0];
        my $port2 = $ports->[1];
        
        my $host1 = $port1->device;
        my $host2 = $port2->device;
        
        my $conntype = $conn->type;
        
        my %edge_attrs = (
                'from'          =>  $host1->name,
                'to'            =>  $host2->name,
                'headclip'      =>  'true',
                'tailclip'      =>  'true'
                );
        
        if (defined($edge_labels)) {
                $edge_attrs{label} =   $host1->name . '/' . $port1->desc . '-->' .
                                     $host2->name . '/' . $port2->desc;
                $edge_attrs{labelangle} = 0;
        }
            
        if ($conntype eq 'Cable') {
            $edge_attrs{color} = "red";
        } elsif ($conntype eq 'TrunkCable') {
            $edge_attrs{color} = "blue";
        } else {
            $edge_attrs{color} = "green";
        }
        
        $g->add_edge(\%edge_attrs);
    }
    
    return $g;
    
}


sub results {
    my $self = shift;
    
    if (@_) {
        $self->{RESULTS} = shift;
    }
    
    return $self->{RESULTS};
}

1;