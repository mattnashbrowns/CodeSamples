package Fenrir::Connection;

use strict;

sub new {
    my $junk = shift;
    my $self = {};
    $self->{INTERFACES} = [];
    my $int1 = shift;
    my $int2 = shift;
    my $type = shift;

    #still need to check to see that these are the right kind of object
    push @{ $self->{INTERFACES} }, $int1;
    push @{ $self->{INTERFACES} }, $int2;
    $self->{TYPE} = $type;
    bless($self);
    return $self;
}

sub interfaces {
    my $self = shift;
    my @tempary = @{$self->{INTERFACES}};
    return \@tempary;
}

sub type {
    my $self = shift;
    return $self->{TYPE};
}

sub id {
    my $self = shift;
    if (@_) {
        $self->{ID} = shift;    
    }
    
    return $self->{ID};
}

1;