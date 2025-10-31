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


$Sent_no = $ARGV[0];

while($in = <STDIN>){
     chomp($in);
     $wrd_ana = $in;
     $sent = "";

          $cat = "ajFAwa";
          ($cat, $sent) = &get_cat($wrd_ana);

          if($cat ne "ajFAwa"){

           if($wrd_ana =~ /<word:[^>\-]+\->/) { $pUrvapaxa = "y";} else {$pUrvapaxa = "n";}
           if($wrd_ana =~ /<word:-/) { $uwwarapaxa = "y";} else {$uwwarapaxa = "n";}

           if($pUrvapaxa eq "y") { $wrd_ana =~ s/<level:([0-4])>/<lifgam:a><viBakwiH:0><vacanam:a><level:$1>/;}

	   #if($cat eq "samAsa") { $wrd_ana =~ s/<vargaH:[^>]+>.*<level:0>//;}

           $wrd_ana =~ s/<vargaH:[^>]+>//; $wrd_ana =~ s/<level:[0-4]>//g;

           $wrd_ana =~ s/<rt:([^>]*)>/<rt:$1><pUrvapaxa:$pUrvapaxa><uwwarapaxa:$uwwarapaxa>/;

           if(($wrd_ana !~ /<upasarga:/) && (($cat eq "kqw") || ($cat eq "wif") || ($cat eq "avykqw"))){
                $wrd_ana =~ s/(<uwwarapaxa:[^>]+>)</$1<upasarga:X></;
           }
           if(($wrd_ana !~ /<sanAxi_prawyayaH:/) && (($cat eq "kqw") || ($cat eq "wif") || ($cat eq "avykqw"))){
                $wrd_ana =~ s/(<upasarga:[a-zA-Z_]+>)</$1<sanAxi_prawyayaH:X></;
           }

 
           $wrd_ana =~ s/^([^<]+)$//g;
           $wrd_ana =~ s/<relata_pos:([0-9]+)\.([0-9]+)>/(relata_pos_id $1) (relata_pos_cid $2)/g;
           $wrd_ana =~ s/<([^:]+):([^>]+)>/($1 $2)/g;
           $wrd_ana =~ s/<relata_pos:>/(relata_pos_id 0) (relata_pos_cid 0)/g;
           $wrd_ana =~ s/<rel_nm:>/(rel_nm X)/g;
       	   $wrd_ana =~ s/<([^:]+):>/($1 X)/g;
           $wrd_ana =~ s/\$//g;

           #print $sent, " (sid $Sent_no)",$wrd_ana,")\n";
           print $sent, $wrd_ana,")\n";
       }
}


sub get_cat{
    my($wrd_ana) = @_;

    my($cat,$sent);

          $sent = "";
          if($wrd_ana =~ /<waxXiwa_prawyayaH.*waxXiwa_rt/) {
              $cat="waxXiwa";
              $sent = "(waxXiwa ";
          } elsif($wrd_ana =~ /<waxXiwa_prawyayaH.*/) {
              $cat="waxXiwa";
              $sent = "(waxXiwa ";
          } elsif($wrd_ana =~ /<vargaH:avy>.*<kqw_prawyayaH/) {
              $cat="kqw";
              $sent = "(avykqw ";
          } elsif($wrd_ana =~ /<kqw_prawyayaH.*/) {
              $cat="kqw";
              $sent = "(kqw ";
          } elsif($wrd_ana =~ /<vargaH:(nA|sarva|pUraNam|saMKyeyam|saMKyA)/) {
              $cat="sup";
              $sent = "(sup ";
          } elsif($wrd_ana =~ /<vargaH:sapUpa/) {
              $cat="sup";
              $sent = "(sup ";
          } elsif($wrd_ana =~ /<vargaH:avy><waxXiwa_prawyayaH:/) {
              $cat="avywaxXiwa";
              $sent = "(avywaxXiwa ";
          } elsif($wrd_ana =~ /<vargaH:avy/) {
              $cat="avy";
              $sent = "(avy ";
          } elsif($wrd_ana =~ /<gaNaH:/) {
              $cat="wif";
              $sent = "(wif ";
          } else {
              $cat = "ajFAwa";
              $sent = "";
          }

  ($cat,$sent);
}
1;
