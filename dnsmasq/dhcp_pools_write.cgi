#!/usr/bin/perl
use strict;
use warnings;
require 'dnsmasq-lib.pl';

our (%in, %config, %dnsmconfig);

&ReadParse();

# Get the config file
my $config_filename = $config{config_file};
my $config_file = &read_file_lines($config_filename);
&parse_config_file(\%dnsmconfig, \$config_file, $config_filename);

# Debug logging to see what's being received
&webmin_debug_log("Save CGI - Input", "All input: " . join(", ", map { "$_ => $in{$_}" } keys %in));

# Collect values from the form fields
my $start_ip = $in{'start_ip'};
my $end_ip = $in{'end_ip'};
my $lease_time = $in{'lease_time'};

# Construct the DHCP range value in the correct format
#my $val = "dhcp-range=" . $start_ip . "," . $end_ip . "," . $lease_time;
if ($in{'add_new_range'}) {
    my $prefix = "dhcp-range";
    my $val .= $start_ip . "," . $end_ip . "," . $lease_time;
    # Add to configuration
    &add_to_list($prefix,$val);
}

# Handle deletions
if ($in{'delete_sel_dhcp_range'}) {
    my @sel = split(/\0/, $in{'sel'});
    if (@sel) {
        &webmin_debug_log("Save CGI - Delete action", "Selected indices: " . join(", ", @sel));
        &do_selected_action(["dhcp_range"], \@sel, \%dnsmconfig);
        &flush_file_lines();  # Save changes to file
    }
}

&redirect("dhcp_pools.cgi");