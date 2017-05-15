import urllib.request
import json

# vehicles
url = "https://api.worldoftanks.asia/wot/encyclopedia/vehicles/?application_id=demo&language=en&page_no="
for i in range(1, 6+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("vehicles/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

#suspensions
url = "https://api.worldoftanks.asia/wot/encyclopedia/modules/?application_id=demo&language=en&type=vehicleChassis&extra=default_profile&page_no="
for i in range(1, 9+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("modules/suspensions/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

#turrets
url = "https://api.worldoftanks.asia/wot/encyclopedia/modules/?application_id=demo&language=en&type=vehicleTurret&extra=default_profile&page_no="
for i in range(1, 6+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("modules/turrets/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

#guns
url = "https://api.worldoftanks.asia/wot/encyclopedia/modules/?application_id=demo&language=en&type=vehicleGun&extra=default_profile&page_no="
for i in range(1, 6+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("modules/guns/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

#engines
url = "https://api.worldoftanks.asia/wot/encyclopedia/modules/?application_id=demo&language=en&type=vehicleEngine&extra=default_profile&page_no="
for i in range(1, 6+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("modules/engines/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

#radios
url = "https://api.worldoftanks.asia/wot/encyclopedia/modules/?application_id=demo&language=en&type=vehicleRadio&extra=default_profile&page_no="
for i in range(1, 2+1):
	c = urllib.request.urlopen(url + str(i))
	d = json.loads(c.read().decode("utf-8"))
	f = open("modules/radios/%d" %i, "w")
	json.dump(d["data"], f, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))

	