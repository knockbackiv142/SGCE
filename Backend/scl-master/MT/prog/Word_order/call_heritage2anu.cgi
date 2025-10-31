#!/usr/bin/perl

#  Copyright (C) 2017-2025 Amba Kulkarni (ambapradeep@gmail.com)
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
#use strict;
#use warnings;

require "../../../paths.pl";
$myPATH="$GlblVar::CGIDIR/$GlblVar::SCL_CGI/";
require "$myPATH/cgi_interface.pl";


print "Content-type:text/html;-expires:60*60*24;charset:UTF-8\n\n";

 my %param = &get_parameters();

 my $buffer = "";
 my $display = "";
 my $field_nm = "";

read(STDIN, $b, $ENV{'CONTENT_LENGTH'});

 $display = $param{DISPLAY};
 my $hash_count = keys %param;
 for (my $i = 1; $i <= $hash_count; $i++) {
       $field_nm = "field".$i;
       $buffer .= $param{$field_nm};
 }
 my $pid = $$."_1";
 if (-d "$GlblVar::TFPATH/tmp_in$pid") {
	system ("rm -rf $GlblVar::TFPATH/tmp_in$pid");
 }
 chomp($buffer);
 $buffer =~ s/[ ]+$//;
 system("mkdir -p $GlblVar::TFPATH/tmp_in$pid");
system("echo '$buffer' | $myPATH/MT/prog/Heritage_morph_interface/Heritage2anusaaraka_morph.sh $myPATH $GlblVar::TFPATH $pid");
#system("cp $GlblVar::TFPATH/tmp_in$pid/in$pid.out $GlblVar::TFPATH/tmp_in$pid/in$pid.out.orig");
#system("cut -f1-7 $GlblVar::TFPATH/tmp_in$pid/in$pid.out > $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp1_7");
#system("cut -f3,8 $GlblVar::TFPATH/tmp_in$pid/in$pid.out | tr '\t' '=' > $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp");
#system("$myPATH/MT/prog/prune/prune.sh $myPATH < $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp | sed '1,\$s/.*=//' > $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp8");
#system("paste $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp1_7 $GlblVar::TFPATH/tmp_in$pid/in${pid}_tmp8 > $GlblVar::TFPATH/tmp_in$pid/in${pid}.out");
#system("cut -f4 $GlblVar::TFPATH/tmp_in$pid/in${pid}.out | tr '\n' ' ' > $GlblVar::TFPATH/tmp_in$pid/wor.$pid");
#system("echo -n \"<s> \"> $GlblVar::TFPATH/in$pid; cat $GlblVar::TFPATH/tmp_in$pid/wor.$pid >> $GlblVar::TFPATH/in$pid; echo \"<\/s>\" >> $GlblVar::TFPATH/in$pid");

if($display eq "") { $display = "DEV";}

#system("$GlblVar::TIMEOUT $myPATH/MT/prog/shell/anu_skt_hnd.sh $myPATH/ tmp_in${pid}/in$pid $GlblVar::TFPATH hi $display GH Full Sloka 1 2> $GlblVar::TFPATH/tmp_in$pid/err$pid");
system("$GlblVar::TIMEOUT $myPATH/MT/prog/shell/anu_skt_hnd.sh $myPATH/ tmp_in${pid}/in$pid $GlblVar::TFPATH hi $display Heritage_manual Full Sloka 1 2> $GlblVar::TFPATH/tmp_in$pid/err$pid");

system("$myPATH/MT/prog/interface/display_output.pl $myPATH $GlblVar::TFPATH $display $pid NIL A $GlblVar::SCL_HTDOCS $GlblVar::SCL_CGI");

