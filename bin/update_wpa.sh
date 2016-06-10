cat tmp/wpaconf >> /etc/wpa_supplicant/wpa_supplicant.conf
killall -HUP wpa_supplicant
