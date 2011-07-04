package Fenrir::Schema::Result::Connections;
  use base qw/DBIx::Class::Core/;

__PACKAGE__->table('Connections');
__PACKAGE__->source_name('Connections');
#__PACKAGE__->add_columns(qw/ ConnID ConnectionType PortID1 PortID2  /);
__PACKAGE__->add_columns(
        ConnID =>
            {   
            	accessor            =>  'connection',
                data_type           =>  'integer',
                size                =>  16,
                is_nullable         =>  0,
                is_auto_increment   =>  0,
            },
        ConnectionType =>
            {   
            	accessor			=>	'conntype',
            	data_type           =>  'varchar',
                size                =>  10,
                is_nullable         =>  0,
                is_auto_increment   =>  0,
                default_value       => ''
                
            },
        Port1ID =>
            {   
            	accessor			=>	'portone',
            	data_type           =>  'integer',
                size                =>  16,
                is_nullable         =>  0,
                is_auto_increment   =>  0
            },
        Port2ID =>
            {   
            	accessor			=>	'porttwo',
            	data_type           =>  'integer',
                size                =>  16,
                is_nullable         =>  0,
                is_auto_increment   =>  0
            }
        );
            
__PACKAGE__->set_primary_key('ConnID');
__PACKAGE__->has_many(
        port1 => 'Fenrir::Schema::Result::Ports',
        {"foreign.PortID" => "self.Port1ID"}
        );
__PACKAGE__->has_many(
        port2 => 'Fenrir::Schema::Result::Ports',
        {"foreign.PortID" => "self.Port2ID"}
        );

1;