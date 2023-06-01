#!/usr/bin/perl
#
#    DNSMasq Webmin Module - dns.cgi; basic DNS config     
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

sub show_dns_settings {
    my @links = ();
    my @titles = ();
    my @icons = ();

    my @buttons = (
        {
            "link" => "dns_basic.cgi",
            "title" => $text{"index_dns_settings_basic"},
            "icon" => "basic.gif"
        },
        {
            "link" => "dns_servers.cgi",
            "title" => $text{"index_dns_servers"},
            "icon" => "servers.gif"
        },
        {
            "link" => "dns_iface.cgi",
            "title" => $text{"index_dns_iface_settings"},
            "icon" => "network.gif"
        },
        {
            "link" => "dns_alias.cgi",
            "title" => $text{"index_dns_alias_settings"},
            "icon" => "alias.gif"
        },
        {
            "link" => "dns_addn_config.cgi",
            "title" => $text{"index_dns_addn_config"},
            "icon" => "files.gif"
        },
    );
    local $i;
    for ($i = 0; $i < @buttons; $i++ ) {
        push(@links, $buttons[$i]->{"link"} );
        push(@titles, $buttons[$i]->{"title"} );
        push(@icons, "images/" . ($current_theme ? "theme/" : "") . $buttons[$i]->{"icon"} );
    }

    print &icons_table(\@links, \@titles, \@icons);
    # print icons_table(@links, @titles);
    # &footer("/", $text{"index"});
}
1;
# uses the index entry in /lang/en



## if subroutines are not in an extra file put them here


### END of index.cgi ###.