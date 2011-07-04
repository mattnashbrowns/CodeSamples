package Fenrir::Schema::Result::Ports;

use base qw/DBIx::Class::Core/;

__PACKAGE__->table('Ports');
__PACKAGE__->source_name('Ports');
#__PACKAGE__->add_columns(qw/ PortID Port Name Description IPAddress HostID  /);

__PACKAGE__->add_columns(
        PortID      =>
        {
            accessor            =>      'port',
            data_type           =>      'integer',
            size                =>      16,
            is_nullable         =>      0,
            is_auto_increment   =>      0
        },
        PortName    =>
        {
        	accessor			=>		'name',
            data_type           =>      'varchar',
            size                =>      30,
            is_nullable         =>      0,
            is_auto_increment   =>      0,
            default_value       =>      ''
        },
        PortDescription         =>
        {
        	accessor			=>		'descrip',
            data_type           =>      'varchar',
            size                =>      30,
            is_nullable         =>      0,
            is_auto_increment   =>      0,
            default_value       =>      ''
        },
        PortString              =>
        {
        	accessor			=>		'string',
            data_type           =>      'varchar',
            size                =>      60,
            is_nullable         =>      0
        },
        DevID                  =>
        {
        	accessor			=>		'devid',
            data_type           =>      'integer',
            size                =>      16,
            is_nullable         =>      0,
            is_auto_increment   =>      0
        },
        IPAddress               =>
        {
        	accessor			=>		'ip',
            data_type           =>      'varchar',
            size                =>      20,
            is_nullable         =>      1,
            is_auto_increment   =>      0,
            default_value       =>      ''
        },
        Connection              =>
        {
            accessor            =>      'connection',
            data_type           =>      'integer',
            size                =>      16,
            is_nullable         =>      1,
            is_auto_increment   =>      0
        }
);

__PACKAGE__->set_primary_key('PortID');
__PACKAGE__->belongs_to(
        "device",
        'Fenrir::Schema::Result::Devices',
        "DevID"
        );
__PACKAGE__->belongs_to(
        "connection",
        'Fenrir::Schema::Result::Connections',
        "Connection"
        );
1;