=pod
Fenrir::Device represents a single device -- a router or a switch

=cut

package Fenrir::Device;

=over
=item new()
Null constructor

=back
=cut
sub new {
    my $self = {};
    $self->{NAME} = undef;
    $self->{IP} = undef;
    $self->{NETMASK} = undef;
    bless($self);
    return $self;
}

=over
=item ip(CIDR)
=item ip()
With no argument, returns the ip address/host bits (a.b.c.d/x)
With an argument, sets the ip address/host bits IF VALID -- otherwise does nothing

=back
=cut
sub ip {
    my $self = shift;
    if (@_) {
        my $cidr = shift;
        #Validate properly formed CIDR address
        #if ($cidr =~ m#((25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)(/(3[012]|[12]\d|\d))#) {
        $self->{IP} = $cidr;
        #}
    }

    return $self->{IP};
}

sub name {
    my $self = shift;
    if (@_) {
        $self->{NAME} = shift;
    }
    
    return $self->{NAME};
}

sub type {
    my $self = shift;
    if (@_) {
        $self->{TYPE} = shift;
    }
    
    return $self->{TYPE};
}

sub id {
    my $self = shift;
    if (@_) {
        $self->{ID} = shift;
    }
    
    return $self->{ID};
}

sub netmask {
    my $self = shift;
    
    if (@_) {
        $self->{NETMASK} = shift;
    }
    
    return $self->{NETMASK};
}
1;