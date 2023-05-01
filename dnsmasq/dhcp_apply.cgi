#!/usr/bin/perl
#
#    DNSMasq Webmin Module - dhcp_apply.cgi; update misc DHCP info     
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

do '../web-lib.pl';
do '../ui-lib.pl';
do 'dnsmasq-lib.pl';

$|=1;
&init_config("DNSMasq");

%access=&get_module_acl;

## put in ACL checks here if needed


## sanity checks


## Insert Output code here
# read config file
$config_filename = $config{config_file};
$config_file = &read_file_lines( $config_filename );
# pass into data structure
&parse_config_file( \%dnsmconfig, \$config_file, \$config_filename );
# read posted data
&ReadParse();
# check for errors in read config
if( $dnsmconfig{"errors"} > 0 ) {
    my $line="error.cgi?line=xx&type=".$text{"err_configbad"};
    &redirect( $line );
    exit;
}
# check for input data errors
if( $in{"bootp-addr"} !~ /^$IPADDR$/ ) {
    my $line="error.cgi?line=".$text{"bootp_address"};
    $line .= "&type=".$text{"err_notip"};
    &redirect( $line );
    exit;
}	
if( $in{"bootp-file"} !~ /^$FILE$/ ) {
    my $line="error.cgi?line=".$text{"bootp_file"};
    $line .= "&type=".$text{"err_filebad"};
    &redirect( $line );
    exit;
}	
if( $in{"bootp-host"} !~ /^$NAME$/ ) {
    my $line="error.cgi?line=".$text{"bootp_host"};
    $line .= "&type=".$text{"err_hostbad"};
    &redirect( $line );
    exit;
}	
if( $in{"max-leases"} !~ /^$NUMBER$/ ) {
    my $line="error.cgi?line=".$text{"max_leases"};
    $line .= "&type=".$text{"err_numbbad"};
    &redirect( $line );
    exit;
}	
if( $in{"leasefile"} !~ /^$FILE$/ ) {
    my $line="error.cgi?line=".$text{"leasefile"};
    $line .= "&type=".$text{"err_filebad"};
    &redirect( $line );
    exit;
}	
# adjust everything to what we got

$action = $in("submit");
if ($action eq "enable") {
}
elsif ($action eq "disable") {
}
elsif ($action eq "delete") {
}

my @files;
if (! grep { /^$/ } ( @files ) ) {
    push @files, $filename;
}
#
# read /etc/ethers
#
&update( $dnsmconfig{"read-ethers"}->{"line"}, "read-ethers", 
    $config_file, ($in{"ethers"} == 1) );

#
# bootp
#
my $line="dhcp-boot=".$in{"bootp-file"}.",".$in{"bootp-host"};
$line .= ",".$in{"bootp-addr"};
&update( $dnsmconfig{"dhcp-boot"}->{"line"}, $line,
    $config_file, ($in{"bootp"} == 1) );
#
# max leases
#
&update( $dnsmconfig{"dhcp-leasemax"}->{"line"}, "dhcp-lease-max=".$in{"dhcp-lease-max"},
    $config_file, ($in{"max=leases"} != 150) );
#
# leases file
# 
&update( $dnsmconfig{"dhcp-leasefile"}->{"line"}, "dhcp-leasefile=".$in{"dhcp-leasefile"},
    $config_file, ($in{"useleasefile"} == 1) );
#
# write file!!
&flush_file_lines();
#
# re-load basic page
&redirect( "dhcp.cgi" );

# 
# sub-routines
#
### END of dhcp_apply.cgi ###.
