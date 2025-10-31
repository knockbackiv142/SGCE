#!/usr/bin/env perl

#  Copyright (C) 2009-2025 Amba Kulkarni (ambapradeep@gmail.com)
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
require "../../../paths.pl";
$myPATH="$GlblVar::CGIDIR/$GlblVar::SCL_CGI";
require "$myPATH/cgi_interface.pl";


package main;

print "Content-type:text/html;-expires:60*60*24;charset:UTF-8\n\n";

my %param = &get_parameters();

      my $dirname=$param{filename};
      my $outscript=$param{outscript};
      my $relations=$param{rel};
      my $sentnum=$param{sentnum};
      my $save=$param{save};
      my $translate=$param{translate};

      $filename = "table_outscript.tsv";
      my $pid = $dirname;
      $pid =~ s/.*\/tmp_in//;

      #  my $cgi = new CGI;
      #print $cgi->header (-charset => 'UTF-8');

      if($relations eq "") { $relations = "''";}

      my $total_filtered_solns = 0;
      if($translate eq "yes") {
	  my $lang = "hi";
          #my $morph = "UoHyd"; We need to do the morph analysis again; since it is already available.
          my $morph = "AVAILABLE";
          my $parse = "AVAILABLE";
          my $text_type = "Sloka";
          my $compound_analysis = "YES";
          $pid =~ /_([0-9])/;
          my $sentno = $1;
          $dirname =~ s/$GlblVar::TFPATH\///;
          system("$myPATH/MT/prog/shell/anu_skt_hnd.sh $myPATH $dirname/in$pid $GlblVar::TFPATH $lang $outscript $morph $parse $text_type $sentno $compound_analysis 2>> $GlblVar::TFPATH/$dirname/err$pid");
	  system("$myPATH/MT/prog/interface/display_output.pl $myPATH $GlblVar::TFPATH $outscript $pid NIL $text_type $GlblVar::SCL_HTDOCS $GlblVar::SCL_CGI");
	  $pid =~ s/_[0-9]//;
	  system("$myPATH/MT/prog/interface/print_table_bottom_menu.pl $myPATH $pid $sent_no $GlblVar::TFPATH $script");
      } else {
      print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
      print "<html xmlns=\"http://www.w3.org/1999/xhtml\">";
      print "<html><head><title>Anusaaraka</title>\n";
      print "<META HTTP-EQUIV=\"Content-Type\" CONTENT=\"text/html; charset=UTF-8\" />\n";
      print "<link href=\"/$GlblVar::SCL_HTDOCS/MT/Sanskrit_style.css\" type=\"text/css\" rel=\"stylesheet\" />\n ";
      print "<style type=\"text/css\">\n";
      print "table { margin-top:20px;}\n";
      print "<\/style>\n";
      print "<\/head>\n<body>\n<div>\n";
      print "<center>\n";
      if($save eq "yes") {
        system("$myPATH/MT/prog/kAraka/mk_summary.pl $myPATH $outscript $dirname/$filename $myPATH/MT/prog/kAraka/list_n $dirname $relations $sentnum $dirname/parser_files/parseop_new.txt $save < $dirname/parser_files/parseop$sentnum.txt");
      } else {
      open(TMP,"<$dirname/parser_files/parseop1.txt") || die "Can't open $dirname/parser_files/parseop1.txt for reading";
      @tmp = <TMP>;
      close(TMP);
      if($tmp[0] =~/Total Complete Solutions=([0-9]+)/){
         $total_filtered_solns = $1;
         print "<h2> Summary of Complete Parses <\/h2>\n";
      } else {
         print "<h2> Summary of Possible Relations <\/h2>\n";
      }
        system("$myPATH/MT/prog/kAraka/mk_summary.pl $myPATH $outscript $dirname/$filename $myPATH/MT/prog/kAraka/list_n $dirname $relations $sentnum $dirname/parser_files/parseop_new.txt $save < $dirname/parser_files/parseop$sentnum.txt");
      print "<\/center>\n";
      print "<\/div>\n";
      print "<\/body>\n<\/html>\n";
    }
    }
