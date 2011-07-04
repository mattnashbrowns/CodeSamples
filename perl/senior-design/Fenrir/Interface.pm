
=pod

=head1 Fenrir::Interface -- represents an Interface on a Device (a switch or router)

=cut

package Fenrir::Interface;

use Fenrir::Device;
=over
=item new(parent,name,description)
The constructor takes three arguments:
parent is a reference to a Fenrir::Device object
name is the name of the interface (e.g. smplralncr01/01.1)
description is the device's name for the interface (e.g. FastEthernet0/0)

=back
=cut
sub new {
    my $class = shift;
    my $self = {};
    my $parent = shift;
    my $name = shift;
    my $desc = shift;
    my $int_string = shift;

    $self->{PARENT} = $parent;
    $self->{NAME} = $name;
    $self->{DESC} = $desc;
    $self->{IPADDR} = undef;
    $self->{STRING} = $int_string;
    bless($self);
    return $self;
}

=over
=item name()
With no argument, returns the name of the interface
With an argument, sets the name of the interface
=back
=cut

sub name {
    my $self = shift;
    if (@_) { $self->{NAME} = shift }
    return $self->{NAME};
}

sub desc {
    my $self = shift;
    if (@_) { $self->{DESC} = shift }
    return $self->{DESC};
}

=over
=item device()
With no argument, returns a reference to the parent Fenrir::Device object
With an argument, sets the 

=back
=cut

sub device {
    my $self = shift;
    my $hostname;

    #Check to make sure that the passed reference is a Fenrir::Device before setting
    if (@_) { 
        $hostname = shift;
        $self->{PARENT} = $hostname;
    }

    return $self->{PARENT};
}

sub ip_addr {
    my $self = shift;

    if (@_) {
        $self->{IPADDR} = shift;
    }

    return $self->{IPADDR};
}

sub int_string {
    my $self = shift;
    if (@_) {
        $self->{STRING} = shift;
    }
    
    return $self->{STRING};
}

sub id {
    my $self = shift;
    if (@_) {
        $self->{ID} = shift;
    }   
    
    return $self->{ID};
}

1;
