#!/usr/bin/perl
#
#    DNSMasq Webmin Module - tftp_bootp.cgi; TFTP/Bootp config
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

## put in ACL checks here if needed

my $config_filename = $config{config_file};
my $config_file = &read_file_lines( $config_filename );

&parse_config_file( \%dnsmconfig, \$config_file, $config_filename );
# read posted data
&ReadParse();

my ($error_check_action, $error_check_result) = &check_for_file_errors( $0, $text{"index_title"}, \%dnsmconfig );
if ($error_check_action eq "redirect") {
    &redirect ( $error_check_result );
}

&ui_print_header($text{"index_tftp_boot_pxe_settings"}, $text{"index_title"}, undef, "intro", 1, 0, 0, &restart_button());
print &header_js();
print $error_check_result;

my $returnto = $in{"returnto"} || "tftp_bootp.cgi";
my $returnlabel = $in{"returnlabel"} || $text{"index_tftp_boot_pxe_settings"};
my $apply_cgi = "tftp_bootp_apply.cgi";

my @page_fields = ();
foreach my $configfield ( @conft_b_p ) {
    next if ( %dnsmconfigvals{"$configfield"}->{"page"} ne "2" );
    push( @page_fields, $configfield );
}

&show_basic_fields( \%dnsmconfig, "tftp_bootp", \@page_fields, $apply_cgi, $text{"index_tftp_boot_pxe_settings"} );

&show_other_fields( \%dnsmconfig, "tftp_bootp", \@page_fields, $apply_cgi, " " );

print &ui_hr();

&show_field_table("bootp_dynamic", $apply_cgi, $text{"_networkid"}, \%dnsmconfig, 1);

print &add_js();

&ui_print_footer("index.cgi?tab=tftp", $text{"index_tftp_settings"}, "index.cgi?tab=dns", $text{"index_dns_settings"});

### END of tftp_bootp.cgi ###.
