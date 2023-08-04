#!/usr/bin/perl
#
#    DNSMasq Webmin Module - # TODO start.cgi; start DNSmasq
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

&header($text{"index_title"}, "", , "intro", 1, 0, 0, &restart_button());

&ReadParse();

## Insert Output code here
# output as web page

&error_setup($text{'start_err'});
$access{'stop'} || &error($text{'start_ecannot'});
$err = &start_dnsmasq();
&error($err) if ($err);
&webmin_log("start");
&redirect($in{'returnto'});

### END of start.cgi ###.