#!/usr/bin/perl
#
#    DNSMasq Webmin Module - dhcp_range_apply.cgi; update DHCP range info     
#    Copyright (C) 2023 by Loren Cress
#    
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.

require 'dnsmasq-lib.pl';

# For debugging
use Data::Dumper;
&webmin_debug_log("DHCP Range Apply - Input", Dumper(\%in));

my $config_filename = $config{config_file};
my $config_file = &read_file_lines($config_filename);

&parse_config_file(\%dnsmconfig, \$config_file, $config_filename);
&ReadParse();

my $returnto = $in{"returnto"} || "dhcp_range.cgi";
my $returnlabel = $in{"returnlabel"} || $dnsmasq::text{"index_dhcp_range"};

sub eval_input_fields {
    # =[tag:<tag>[,tag:<tag>],][set:<tag>,]<start-addr>[,<end-addr>|<mode>][,<netmask>[,<broadcast>]][,<lease time>]
    my ($is_new) = @_;
    my $par_prefix = ($is_new == 1 ? "new_" : "") . "dhcp_range_";
    
    # Check if IPv4 or IPv6
    my $ipversion = $in{$par_prefix . "ipversion"} || "4";
    return "" if (!$in{$par_prefix . "start"});
    
    my $val = "";
    
    # Handle tags first
    if ($in{$par_prefix . "tag"}) {
        my @tags = split(/\s*,\s*/, $in{$par_prefix . "tag"});
        foreach my $tag (@tags) {
            next if !$tag;
            $val .= ($val ? "," : "") . 
                   ($tag !~ /^tag:/ ? "tag:" : "") . 
                   $tag;
        }
    }
    
    # Handle set tag
    if ($in{$par_prefix . "settag"}) {
        $val .= ($val ? "," : "") . 
               ($in{$par_prefix . "settag"} !~ /^set:/ ? "set:" : "") . 
               $in{$par_prefix . "settag"};
    }
    
    # Start address is required
    if ($in{$par_prefix . "start"}) {
        if ($ipversion eq "4" && !&check_ipaddress($in{$par_prefix . "start"})) {
            &error($dnsmasq::text{'err_ipbad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "start"};
    }
    
    # End address
    if ($in{$par_prefix . "end"}) {
        if ($ipversion eq "4" && !&check_ipaddress($in{$par_prefix . "end"})) {
            &error($dnsmasq::text{'err_ipbad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "end"};
    }
    
    # IPv4 specific options
    if ($ipversion eq "4") {
        # Netmask
        if ($in{$par_prefix . "mask"}) {
            if (!&check_ipaddress($in{$par_prefix . "mask"})) {
                &error($dnsmasq::text{'err_netmaskbad'});
            }
            $val .= ($val ? "," : "") . $in{$par_prefix . "mask"};
        }
        
        # Broadcast
        if ($in{$par_prefix . "broadcast"}) {
            if (!&check_ipaddress($in{$par_prefix . "broadcast"})) {
                &error($dnsmasq::text{'err_broadcastbad'});
            }
            $val .= ($val ? "," : "") . $in{$par_prefix . "broadcast"};
        }
    }
    
    # IPv6 specific options
    if ($ipversion eq "6") {
        # Prefix length
        if ($in{$par_prefix . "prefix-length"}) {
            if ($in{$par_prefix . "prefix-length"} !~ /^\d+$/ || 
                $in{$par_prefix . "prefix-length"} > 128) {
                &error($dnsmasq::text{'err_prefixbad'});
            }
            $val .= ($val ? "," : "") . $in{$par_prefix . "prefix-length"};
        }
    }
    
    # Boolean options
    my @bool_options = ("static", "ra-only", "ra-names", "ra-stateless", 
                       "slaac", "ra-advrouter", "off-link");
    foreach my $opt (@bool_options) {
        if ($in{$par_prefix . $opt} eq "1") {
            $val .= ($val ? "," : "") . $opt;
        }
    }
    
    # Lease time
    if ($in{$par_prefix . "leasetime"}) {
        if ($in{$par_prefix . "leasetime"} !~ /^\d+[mhdw]?$|^infinite$/) {
            &error($dnsmasq::text{'err_leasetimebad'});
        }
        $val .= ($val ? "," : "") . $in{$par_prefix . "leasetime"};
    }
    
    &webmin_debug_log("DHCP Range Apply - Generated Value", $val);
    return $val;
}

# Handle new entries
if ($in{'new_dhcp_range_start'}) {
    my $val = &eval_input_fields(1);
    if ($val) {
        &webmin_debug_log("DHCP Range Apply - Adding new entry", $val);
        &add_to_list("dhcp-range", $val);
    }
}
# Handle edited entries
elsif ($in{"cfg_idx"} ne "") {
    my $val = &eval_input_fields(0);
    if ($val) {
        my $item = $dnsmconfig{"dhcp-range"}[$in{"cfg_idx"}];
        &webmin_debug_log("DHCP Range Apply - Updating entry", 
                         "Index: " . $in{"cfg_idx"} . ", Value: " . $val);
        &save_update($item->{"file"}, $item->{"lineno"}, "dhcp-range=" . $val);
    }
}
# Handle enable/disable/delete actions
else {
    my @sel = split(/\0/, $in{'sel'});
    if (@sel) {
        &webmin_debug_log("DHCP Range Apply - Bulk action", 
                         "Selection: " . join(",", @sel));
        &do_selected_action(["dhcp_range"], \@sel, \%dnsmconfig);
    }
}

# Redirect back to the main page with the correct tab
&redirect($returnto . "?ipversion=" . ($in{"ipversion"} || "ip4"));
