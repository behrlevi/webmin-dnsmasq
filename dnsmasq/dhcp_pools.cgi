#!/usr/bin/perl
use WebminCore;
require 'dnsmasq-lib.pl';

init_config();
my $config_filename = $config{config_file};
my $config_file = &read_file_lines( $config_filename );
&parse_config_file( \%dnsmconfig, \$config_file, $config_filename );

&ReadParse();
my ($error_check_action, $error_check_result) = &check_for_file_errors( $0, $dnsmasq::text{"index_dhcp_range"}, \%dnsmconfig );
if ($error_check_action eq "redirect") {
    &redirect ( $error_check_result );
}

my ($section, $page) = &get_context($0);

print $error_check_result;

our $internalfield = "dhcp_range";
my $configfield = &internal_to_config($internalfield);
my $definition = %configfield_fields{$internalfield};
my $formidx = 0;

sub show_ip_range_list {
    my ($ipver, $formidx) = @_;
    my $version_excluded = ($ipver == 4 ? 6 : 4);
    my $edit_link;
    my $hidden_edit_input_fields;
    my @column_headers = ( "", $dnsmasq::text{"enabled"}, );
    my @newfields = ( "ipversion" );
    foreach my $param ( @{$definition->{"param_order"}} ) {
        next if ($definition->{$param}->{"ipversion"} == $version_excluded);
        push( @newfields, $param );
        if ($definition->{$param}->{"valtype"} eq "bool") {
            push( @column_headers, $dnsmasq::text{"p_label_val_short_" . $param} . &ui_help($dnsmasq::text{"p_label_val_" . $param}) );
        }
        else {
            push( @column_headers, $definition->{$param}->{"label"} );
        }
    }
    my @editfields = ( "cfg_idx", @newfields );
    my $formid = $internalfield . "_" . $ipver . "_form";
    my @tds = ( &get_class_tag($td_label_class), &get_class_tag($td_left_class), &get_class_tag($td_left_class) ); # extra column for set-tags
    foreach my $param ( @newfields ) {
        push( @tds, &get_class_tag($td_left_class) );
    }
    my @list_link_buttons = &list_links( "sel", $formidx );
    my ($add_button, $hidden_add_input_fields) = &add_item_button(&text("add_", $dnsmasq::text{"_range"}), $internalfield, $dnsmasq::text{"p_desc_$internalfield"}, $formid, \@newfields, "ipversion=ip" . $ipver );
    push(@list_link_buttons, $add_button);

    my $count = -1;
    print &ui_form_start("dhcp_pools_write.cgi", "post");
    print &ui_columns_start( \@column_headers, 100, undef, undef, &ui_columns_header( [ &show_title_with_help($internalfield, $configfield) ], [ 'class="table-title" colspan=' . @column_headers ] ), 1 );
    foreach my $item ( @{$dnsmconfig{$configfield}} ) {
        $count++;
        next if ($item->{"val"}->{"ipversion"} == $version_excluded);
        local @cols;
        push ( @cols, &ui_checkbox("enabled", "1", "", $item->{"used"}?1:0, undef, 1) );
        my @vals = ( );
        foreach my $param ( @{$definition->{"param_order"}} ) {
            next if ($definition->{$param}->{"ipversion"} == $version_excluded);
            if ($definition->{$param}->{"arr"} == 1) {
                push( @vals, join($definition->{$param}->{"sep"}, @{$item->{"val"}->{$param}}) );
            }
            elsif ($definition->{$param}->{"valtype"} eq "bool") {
                push( @vals, &ui_checkbox(undef, "1", "", $item->{"val"}->{$param} ));
            }
            else {
                push( @vals, $item->{"val"}->{$param} );
            }
        }
        foreach my $val ( @vals ) {
            # first call to &edit_item_link should capture link and fields; subsequent calls (1 for each field) only need the link
            if ( ! $hidden_edit_input_fields) {
                ($edit_link, $hidden_edit_input_fields) = &edit_item_link($val, $internalfield, $dnsmasq::text{"p_desc_$internalfield"}, $count, $formid, \@editfields, $item->{"cfg_idx"}, ($in{"show_validation"} ? "show_validation=" . $in{"show_validation"} : "") . "&ipversion=ip" . $ipver);
            }
            else {
                ($edit_link) = &edit_item_link($val, $internalfield, $dnsmasq::text{"p_desc_$internalfield"}, $count, $formid, \@editfields, $item->{"cfg_idx"}, ($in{"show_validation"} ? "show_validation=" . $in{"show_validation"} : "") . "&ipversion=ip" . $ipver);
            }
            push( @cols, $edit_link );
        }
        print &ui_clickable_checked_columns_row( \@cols, \@tds, "sel", $count );
    }
    print &ui_columns_end();
    print &ui_submit($dnsmasq::text{"button_delete_sel"}, "delete_sel_dhcp_range");
    print $hidden_add_input_fields;
    print $hidden_edit_input_fields;
    print &ui_form_end();
}

# Display header
&ui_print_header(undef, $dnsmasq::text{'dhcp_pools_title'}, "");

# Create simple form
print &ui_form_start("dhcp_pools_write.cgi", "post");
print &ui_table_start($text{'add_range'}, undef, 2);

# Add manual entry fields
print &ui_table_row(
    "<table border='0' cellspacing='0' cellpadding='0'><tr>" .
    "<td>Start IP: " . &ui_textbox("start_ip", $config{'start_ip'}, 20) . "</td>" .
    "<td>&nbsp;&nbsp;</td>" .
    "<td>End IP: " . &ui_textbox("end_ip", $config{'end_ip'}, 20) . "</td>" .
    "<td>&nbsp;&nbsp;</td>" .
    "<td>Lease Time: " . &ui_textbox("lease_time", $config{'lease_time'}, 20) . "</td>" .
    "</tr></table>",
    undef,  # No header
    1       # Span all columns
);

print &ui_table_end();
print &ui_submit($text{'save'}, "add_new_range");
print &ui_form_end();
#print &ui_form_end([ [ "save", $text{'save'} ] ]);

&show_ip_range_list(4, $formidx++);

# Display footer
&ui_print_footer("/", $text{'index'});


#test