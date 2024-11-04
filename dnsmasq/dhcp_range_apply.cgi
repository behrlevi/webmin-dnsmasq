#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use Cwd;
require 'dnsmasq-lib.pl';

our (%in, %config, %dnsmconfig);

# Debug current working directory
print STDERR "\n=== DIRECTORY INFO ===\n";
print STDERR "Initial CWD: " . (getcwd() || "Cannot get CWD") . "\n";

# Try to set working directory to script location
my $script_dir;
BEGIN {
    use File::Basename;
    $script_dir = dirname(__FILE__);
}
chdir($script_dir) or print STDERR "Cannot chdir to $script_dir: $!\n";
print STDERR "Script directory: $script_dir\n";
print STDERR "New CWD: " . (getcwd() || "Cannot get CWD") . "\n";

print STDERR "\n=== REQUEST INFO ===\n";
print STDERR "Request started at: " . scalar(localtime) . "\n";
print STDERR "REQUEST_METHOD: " . $ENV{'REQUEST_METHOD'} . "\n";
print STDERR "CONTENT_TYPE: " . $ENV{'CONTENT_TYPE'} . "\n";
print STDERR "CONTENT_LENGTH: " . $ENV{'CONTENT_LENGTH'} . "\n";

# Make sure we can read POST data
eval {
    &ReadParse();
    print STDERR "\n=== PARSE SUCCESS ===\n";
    print STDERR "Form data parsed successfully\n";
    print STDERR Dumper(\%in);
};
if ($@) {
    print STDERR "\n=== PARSE ERROR ===\n";
    print STDERR "Error parsing form data: $@\n";
    die "Failed to parse form data: $@";
}

# Process the form data if we got here
my $val = $in{"new_dhcp_range_start"};
if ($in{"new_dhcp_range_end"}) {
    $val .= "," . $in{"new_dhcp_range_end"};
}
if ($in{"new_dhcp_range_leasetime"}) {
    $val .= "," . $in{"new_dhcp_range_leasetime"};
}

print STDERR "\n=== VALUE INFO ===\n";
print STDERR "Final value to be added: " . (defined $val ? "'$val'" : "undefined") . "\n";

if ($val && $val ne "") {
    eval {
        &add_to_list("dhcp-range", $val);
        print STDERR "Successfully added to list\n";
    };
    if ($@) {
        print STDERR "Error adding to list: $@\n";
        die "Failed to add to list: $@";
    }
}

&redirect("dhcp_range.cgi");