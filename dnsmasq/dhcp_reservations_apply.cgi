#!/usr/bin/perl
#
#    DNSMasq Webmin Module - dhcp_reservations_apply.cgi; update DHCP reservations     
#    Copyright (C) 2023 by Loren Cress
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    This module based on the DNSMasq Webmin module by Neil Fisher

require "dnsmasq-lib.pl";

## put in ACL checks here if needed

# For debugging
use Data::Dumper;
&webmin_debug_log("DHCP Reservations Apply - Input", Dumper(\%in));

my $config_filename = $config{config_file};
my $config_file = &read_file_lines($config_filename);

&parse_config_file(\%dnsmconfig, \$config_file, $config_filename);
# read posted data
&ReadParse();

my $returnto = $in{"returnto"} || "dhcp_reservations.cgi";
my $returnlabel = $in{"returnlabel"} || $dnsmasq::text{"index_dhcp_settings_basic"};

sub eval_input_fields {
    # =[<hwaddr>][,id:<client_id>|*][,set:<tag>][tag:<tag>][,<ipaddr>][,<hostname>][,<lease_time>][,ignore]
    # "mac", "clientid", "infiniband", "settag", "tag", "ip", "hostname", "leasetime", "ignore"
    my ($is_new) = @_;

    my $par_prefix = ($is_new == 1 ? "new_" : "") . "dhcp_host_";

    # Require at least one identifier
    return "" if (!$in{$par_prefix . "mac"} && 
                 !$in{$par_prefix . "clientid"} && 
                 !$in{$par_prefix . "infiniband"});
    
    my $val = "";

    # Handle MAC address
    if ($in{$par_prefix . "mac"} ne "") {
        if ($in{$par_prefix . "mac"} !~ /^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$/) {
            &error($dnsmasq::text{'err_macbad'});
        }
        $val .= $in{$par_prefix . "mac"};
    }

    # Handle Client ID
    if ($in{$par_prefix . "clientid"} ne "") {
        $val .= ($val ? "," : "") . "id:" . $in{$par_prefix . "clientid"};
    }
    # Handle Infiniband
    elsif ($in{$par_prefix . "infiniband"} ne "") {
        $val .= ($val ? "," : "") . $in{$par_prefix . "infiniband"};
    }

    # Handle Set Tags
    if ($in{$par_prefix . "settag"} ne "") {
        my $settag = "";
        my @tags = split(/\s*,\s*/, $in{$par_prefix . "settag"});
        foreach my $t (@tags) {
            next if !$t;  # Skip empty tags
            $settag .= ($settag ? "," : "") . 
                      ($t !~ /^set:/ ? "set:" : "") . 
                      $t;
        }
        $val .= ($val ? "," : "") . $settag if $settag;
    }

    # Handle Tag
    if ($in{$par_prefix . "tag"} ne "") {
        my $tag = $in{$par_prefix . "tag"};
        $val .= ($val ? "," : "") . 
                ($tag !~ /^tag:/ ? "tag:" : "") . 
                $tag;
    }

    # Handle IP address
    if ($in{$par_prefix . "ip"} ne "") {
        if (!&check_ipaddress($in{$par_prefix . "ip"})) {
            &error($dnsmasq::text{'err_ipbad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "ip"};
    }

    # Handle Hostname
    if ($in{$par_prefix . "hostname"} ne "") {
        if ($in{$par_prefix . "hostname"} !~ /^[a-zA-Z0-9][-a-zA-Z0-9]*$/) {
            &error($dnsmasq::text{'err_hostnamebad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "hostname"};
    }

    # Handle Lease Time
    if ($in{$par_prefix . "leasetime"} ne "") {
        if ($in{$par_prefix . "leasetime"} !~ /^\d+[mhdw]?$|^infinite$/) {
            &error($dnsmasq::text{'err_leasetimebad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "leasetime"};
    }

    # Handle Ignore flag
    if ($in{$par_prefix . "ignore"} eq "1") {
        $val .= ($val ? "," : "") . "ignore";
    }

    &webmin_debug_log("DHCP Reservations Apply - Generated Value", $val);
    return $val;
}

# Handle new entries
if ($in{'new_dhcp_host_mac'} ne "" || 
    $in{'new_dhcp_host_clientid'} ne "" || 
    $in{'new_dhcp_host_infiniband'} ne "") {
    my $val = &eval_input_fields(1);
    if ($val) {
        &webmin_debug_log("DHCP Reservations Apply - Adding new entry", $val);
        &add_to_list("dhcp-host", $val);
    }
}
# Handle edited entries
elsif ($in{"cfg_idx"} ne "") {
    my $val = &eval_input_fields(0);
    if ($val) {
        my $item = $dnsmconfig{"dhcp-host"}[$in{"cfg_idx"}];
        &webmin_debug_log("DHCP Reservations Apply - Updating entry", "Index: " . $in{"cfg_idx"} . ", Value: " . $val);
        &save_update($item->{"file"}, $item->{"lineno"}, "dhcp-host=" . $val);
    }
}
# Handle enable/disable/delete actions
else {
    my @sel = split(/\0/, $in{'sel'});
    if (@sel) {
        &webmin_debug_log("DHCP Reservations Apply - Bulk action", "Selection: " . join(",", @sel));
        &do_selected_action(["dhcp_host"], \@sel, \%dnsmconfig);
    }
}

# Redirect back to the main page
&redirect($returnto);
