
require 'dnsmasq-lib.pl';

# acl_security_form(&options)
# Output HTML for editing security options for the dnsmasq module
sub acl_security_form {

    print "<tr> <td><b>".$text{"acl_root"}."</b></td>\n";
    printf "<td colspan=3><input name=root size=40 value='%s'> %s</td> </tr>\n",
        $_[0]->{'root'}, &file_chooser_button("root", 1);

    print "<tr> <td><b>".$text{"acl_start"}."</b></td>\n";
    printf "<td><input type=radio name=start value=1 %s> %s\n",
        $_[0]->{'start'} ? 'checked' : '', $text{"yes"};
    printf "<input type=radio name=start value=0 %s> %s</td> </tr>\n",
        $_[0]->{'start'} ? '' : 'checked', $text{"no"};

    print "<tr> <td><b>".$text{"acl_restart"}."</b></td>\n";
    printf "<td><input type=radio name=restart value=1 %s> %s\n",
        $_[0]->{'restart'} ? 'checked' : '', $text{"yes"};
    printf "<input type=radio name=restart value=0 %s> %s</td> </tr>\n",
        $_[0]->{'restart'} ? '' : 'checked', $text{"no"};
}

# acl_security_save(&options)
# Parse the form for security options for the dnsmasq module
sub acl_security_save {
    $_[0]->{'root'} = $in{'root'};
    $_[0]->{'start'} = $in{'start'};
    $_[0]->{'restart'} = $in{'restart'};
}

