package Fenrir::Schema::Result::Devices;
  use base qw/DBIx::Class::Core/;

__PACKAGE__->table('Devices');
__PACKAGE__->source_name('Devices');
#__PACKAGE__->add_columns(qw/DevID HostName DeviceType/);
__PACKAGE__->add_columns(
    DevID       =>
        {
            accessor            =>  'device',
            data_type           =>  'integer',
            size                =>  16,
            is_nullable         =>  0,
            is_auto_increment   =>  0
        },
    HostName    =>
        {
        	accessor			=>	'hostname',
            data_type           =>  'varchar',
            size                =>  30,
            is_nullable         =>  0,
            default_value       =>  ''
        },
    DeviceType  =>
        {
        	accessor			=>  'devicetype',
            data_type           =>  'varchar',
            size                =>  20,
            is_nullable         =>  0,
            default_value       =>  ''
        },
    IPAddress   =>
        {
            accessor            =>  'ipaddr',
            data_type           =>  'varchar',
            size                =>  18,
            is_nullable         =>  0,
            default_value       => '0.0.0.0'
        },
    Netmask     =>
        {
            accessor            =>  'netmask',
            data_type           =>  'varchar',
            size                =>  18,
            is_nullable         =>  1,
            default_value       => '255.255.255.0'
        }
);
__PACKAGE__->set_primary_key('DevID');
__PACKAGE__->has_many(
        "ports",
        'Fenrir::Schema::Result::Ports',
        {"foreign.DevID" => "self.DevID"}
        );

1;