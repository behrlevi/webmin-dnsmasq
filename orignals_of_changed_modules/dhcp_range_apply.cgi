#!/usr/bin/perl
require 'dnsmasq-lib.pl';
&ReadParse();

# Get the config file
my $config_filename = $config{config_file};
my $config_file = &read_file_lines($config_filename);
&parse_config_file(\%dnsmconfig, \$config_file, $config_filename);

my $internalfield = "dhcp_host";
my $configfield = &internal_to_config($internalfield);

if ($in{"submit"}) {
    # Handle new/edited values
    my @newfields = ("ipversion");
    foreach my $param (@{$configfield_fields{$internalfield}->{"param_order"}}) {
        next if ($configfield_fields{$internalfield}->{$param}->{"ipversion"} == 6);
        push(@newfields, $param);
    }

    # Build the new config line
    my $val = "";
    if ($in{"mac"}) { $val .= $in{"mac"}; }
    if ($in{"clientid"}) { $val .= ",id:" . $in{"clientid"}; }
    if ($in{"settag"}) { $val .= ",set:" . $in{"settag"}; }
    if ($in{"tag"}) { $val .= ",tag:" . $in{"tag"}; }
    if ($in{"ip"}) { $val .= "," . $in{"ip"}; }
    if ($in{"hostname"}) { $val .= "," . $in{"hostname"}; }
    if ($in{"leasetime"}) { $val .= "," . $in{"leasetime"}; }
    if ($in{"ignore"}) { $val .= ",ignore"; }

    if ($in{"cfg_idx"} ne "") {
        # Update existing entry
        &save_update($config_filename, $dnsmconfig{$configfield}[$in{"cfg_idx"}]->{"lineno"}, "$configfield=$val");
    } else {
        # Add new entry
        &add_to_list($configfield, $val);
    }
}

# Handle enable/disable/delete actions
if (defined($in{"sel"})) {
    my @sel = split(/\0/, $in{"sel"});
    if ($in{"button_disable_sel"} || $in{"button_delete_sel"}) {
        &update_selected($configfield, 
                        $in{"button_disable_sel"} ? "disable" : "delete",
                        \@sel,
                        \%dnsmconfig);
    }
}

&redirect("dhcp_reservations.cgi");
