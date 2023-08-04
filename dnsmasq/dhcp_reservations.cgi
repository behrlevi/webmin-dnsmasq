#!/usr/bin/perl
#
#    DNSMasq Webmin Module - # TODO dhcp_reservations.cgi; DHCP reservations config
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

require 'dnsmasq-lib.pl';

my %access=&get_module_acl;

## put in ACL checks here if needed

my $config_filename = $config{config_file};
my $config_file = &read_file_lines( $config_filename );

&parse_config_file( \%dnsmconfig, \$config_file, $config_filename );

&header($text{"index_title"}, "", "intro", 1, 0, 0, &restart_button(), undef, undef, $text{"index_dhcp_host_reservations"});

my $returnto = $in{"returnto"} || "dhcp_reservations.cgi";
my $returnlabel = $in{"returnlabel"} || $text{"index_dhcp_host_reservations"};
my $apply_cgi = "dhcp_reservations_apply.cgi"; #TODO create this file

my $internalfield = "dhcp_host";
my $configfield = &internal_to_config($internalfield);
my $definition = %configfield_fields{$internalfield};

sub show_reservations() {
    my $edit_link;
    my $hidden_edit_input_fields;
    my $edit_script;
    my @newfields = ( "ipversion" );
    foreach my $param ( @{$definition->{"param_order"}} ) {
        next if ($definition->{$param}->{"ipversion"} == 6);
        push( @newfields, $param );
    }
    my @editfields = ( "idx", @newfields );
    my $formid = $internalfield . "_4_form";
    my $w = 520;
    my $h = 340; # base value
    my $extralines = length($text{"p_man_desc_$internalfield"}) / 75;
    $extralines = ceil($extralines) * 15;
    $h += $extralines;
    my @tds = ( $td_label, $td_left );
    my @column_headers = ( "",
        $text{"enabled"},
        $text{"p_label_val_hostname"}, 
        $text{"p_label_val_ip_address"}, 
        $text{"p_label_val_mac"}, 
        $text{"p_label_val_ignore"}, 
        $text{"p_label_val_tag"}, 
        $text{"p_label_val_leasetime"}, );
    foreach my $param ( @newfields ) {
        push( @tds, $td_left );
        $h = $h + 31;
    }
    # my @list_link_buttons = &list_links( "sel", 0, "dhcp_res_apply.cgi", "dhcp-host=new,0.0.0.0", "dhcp_reservations.cgi", &text("add_", $text{"_host"}) );
    my @list_link_buttons = &list_links( "sel", 3 );
    my ($add_button, $hidden_add_input_fields, $add_new_script) = &add_item_button( &text("add_", $text{"_host"}), $internalfield, $text{"p_desc_$internalfield"}, $w, $h, $formid, \@newfields );
    push(@list_link_buttons, $add_button);

    my $count = 0;
    print &ui_form_start( $apply_cgi, "post", undef, "id='$formid'" );
    print &ui_links_row(\@list_link_buttons);
    print $hidden_add_input_fields . $add_new_script;
    print &ui_columns_start( \@column_headers, 100, undef, undef, &ui_columns_header( [ &show_title_with_help($internalfield, $configfield) ], [ 'class="table-title" colspan=' . @column_headers ] ), 1 );
    foreach my $item ( @{$dnsmconfig{$configfield}} ) {
        local @cols;
        push ( @cols, &ui_checkbox("enabled", "1", "", $item->{"used"}?1:0, undef, 1) );
        my @vals = ( 
            $item->{"val"}->{"hostname"}, 
            $item->{"val"}->{"ip"}, 
            $item->{"val"}->{"infiniband"} . $item->{"val"}->{"clientid"} . $item->{"val"}->{"mac"}, 
            &ui_checkbox("enabled", "1", "", $item->{"val"}->{"ignore_clientid"}?1:0, undef, 1),
            $item->{"val"}->{"tagname"}, 
            $item->{"val"}->{"leasetime"});
        foreach my $val ( @vals ) {
            if ( ! $hidden_edit_input_fields) {
                ($edit_link, $hidden_edit_input_fields, $edit_script) = &edit_item_link($val, $internalfield, $text{"p_desc_$internalfield"}, $count, $formid, $w, $h, \@editfields );
            }
            else {
                ($edit_link) = &edit_item_link($val, $internalfield, $text{"p_desc_$internalfield"}, $count, $formid, $w, $h, \@editfields );
            }
            push( @cols, $edit_link );
        }
        print &ui_checked_columns_row( \@cols, undef, "sel", $count );
        $count++;
    }
    print &ui_columns_end();
    print $hidden_edit_input_fields . $edit_script;
    print &ui_links_row(\@list_link_buttons);
    print "<p>" . $text{"with_selected"} . "</p>";
    print &ui_submit($text{"enable_sel"}, "enable_sel_$internalfield");
    print &ui_submit($text{"disable_sel"}, "disable_sel_$internalfield");
    print &ui_submit($text{"delete_sel"}, "delete_sel_$internalfield");
    print &ui_form_end( );
}

&show_reservations();

print &add_js();

ui_print_footer("index.cgi?mode=dhcp", $text{"index_dhcp_settings"}, "index.cgi?mode=dns", $text{"index_dns_settings"});

### END of dhcp_reservations.cgi ###.
