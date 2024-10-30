#!/usr/bin/perl
require 'dnsmasq-lib.pl';
&ReadParse();

&ui_print_header(undef, $dnsmasq::text{'dhcp_leases_title'}, "");

# Read the DHCP leases file
my $leases_file = "/var/lib/misc/dnsmasq.leases";
my @leases;

if (-r $leases_file) {
    if (open(LEASES, $leases_file)) {
        while (<LEASES>) {
            chomp;
            my ($expires, $mac, $ip, $hostname, $clientid) = split(/\s+/);
            push(@leases, {
                'expires' => $expires ? scalar(localtime($expires)) : $dnsmasq::text{'never'},
                'mac' => $mac || "-",
                'ip' => $ip || "-",
                'hostname' => $hostname || "-",
                'clientid' => $clientid || "-"
            });
        }
        close(LEASES);
    } else {
        print "<p>", &text('dhcp_leases_efile', $!), "</p>";
    }
} else {
    print "<p>", &text('dhcp_leases_none', $leases_file), "</p>";
}

if (@leases) {
    # Sort leases by IP address
    @leases = sort { $a->{'ip'} cmp $b->{'ip'} } @leases;

    print &ui_columns_start([
        $dnsmasq::text{'dhcp_leases_expires'},
        $dnsmasq::text{'dhcp_leases_mac'},
        $dnsmasq::text{'dhcp_leases_ip'},
        $dnsmasq::text{'dhcp_leases_hostname'},
        $dnsmasq::text{'dhcp_leases_clientid'}
    ], 100);

    foreach my $lease (@leases) {
        print &ui_columns_row([
            $lease->{'expires'},
            "<tt>$lease->{'mac'}</tt>",
            "<tt>$lease->{'ip'}</tt>",
            $lease->{'hostname'},
            "<tt>$lease->{'clientid'}</tt>"
        ]);
    }

    print &ui_columns_end();
} else {
    print "<p>", $dnsmasq::text{'dhcp_leases_empty'}, "</p>";
}

&ui_print_footer("", $dnsmasq::text{'index'});
