#!/usr/bin/perl
require 'dnsmasq-lib.pl';
&ReadParse();

# Get the config file
my $config_filename = $config{config_file};
my $config_file = &read_file_lines($config_filename);
&parse_config_file(\%dnsmconfig, \$config_file, $config_filename);

# Define the DHCP range configuration
my $configfield = "dhcp-range";
my $dhcp_range_value = "192.168.66.6,192.168.66.250,1h";

# Check if dhcp-range already exists in the config
my $found = 0;
foreach my $i (0 .. $#{$config_file}) {
    if ($config_file->[$i] =~ /^dhcp-range=/) {
        # Update existing entry
        &save_update($config_filename, $i, "$configfield=$dhcp_range_value");
        $found = 1;
        last;
    }
}

# If no existing entry found, add new one
if (!$found) {
    &add_to_list($configfield, $dhcp_range_value);
}

&redirect("dhcp_range.cgi");