#!/usr/bin/perl

#  Copyright (C) 2017-2021 Amba Kulkarni (ambapradeep@gmail.com)
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either
#  version 2 of the License, or (at your option) any later
#  version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

use utf8;
use strict;
use warnings;

require "../../../paths.pl";
require "$GlblVar::SCLINSTALLDIR/cgi_interface.pl";


require "$GlblVar::SCLINSTALLDIR/converters/convert.pl";

# use CGI qw( :standard );
 
# my $cgi = new CGI;
# print $cgi->header (-charset => 'UTF-8');
 
print "Content-type:text/html;-expires:60*60*24;charset:UTF-8\n\n";

  my %param = &get_parameters();

 my $buffer = "";
 my $display = "";
 my $field_nm = "";

read(STDIN, $b, $ENV{'CONTENT_LENGTH'});

# if (param()){
#foreach my $p (sort keys %param){
#    if($p eq "DISPLAY") { $display = $param{$p};}
#    else {$buffer .= $param{$p};}
    $display = $param{DISPLAY};
    my $hash_count = keys %param;
    for (my $i = 1; $i <= $hash_count; $i++) {
	    $field_nm = "field".$i;
            $buffer .= $param{$field_nm};
    }
 my $pid = $$;
 system("mkdir -p $GlblVar::TFPATH/tmp_in$pid");

 system ("echo '$buffer' > /tmp/SKT_TEMP/abcd");
 system("echo '$buffer' | $GlblVar::SCLINSTALLDIR/SHMT/prog/Heritage_morph_interface/Heritage2anusaaraka_morph.sh $GlblVar::SCLINSTALLDIR > $GlblVar::TFPATH/tmp_in$pid/in$pid.out");
 # system("rm /tmp/abcd");

if($display eq "") { $display = "DEV";}

#system("$GlblVar::SCLINSTALLDIR/SHMT/prog/shell/Heritage_anu_skt_hnd.sh in$pid $GlblVar::TFPATH $display Full Prose NOECHO ND 2> $GlblVar::TFPATH/tmp_in$pid/err$pid");
system("$GlblVar::SCLINSTALLDIR/SHMT/prog/shell/Heritage_anu_skt_hnd.sh in$pid $GlblVar::TFPATH $display Full Sloka NOECHO ND 2> $GlblVar::TFPATH/tmp_in$pid/err$pid");
 #system("$GlblVar::SCLINSTALLDIR/SHMT/prog/shell/Heritage_anu_skt_hnd.sh in$pid $GlblVar::TFPATH $display Full Sloka NOECHO ND 2> $GlblVar::TFPATH/tmp_in$pid/err$pid");

 system("$GlblVar::SCLINSTALLDIR/SHMT/prog/interface/display_anu_out.pl $pid $GlblVar::TFPATH");
# system("$GlblVar::SCLINSTALLDIR/SHMT/prog/interface/display_output.pl $GlblVar::SCLINSTALLDIR $GlblVar::TFPATH $display $pid");

 #}
