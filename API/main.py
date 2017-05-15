import os
import json

vehicles = {}
engines = {}
guns = {}
radios = {}
suspensions = {}
turrets = {}

def load():
	ds = [
		vehicles, 
		engines,
		guns,
		radios,
		suspensions,
		turrets
	]
	base_dirs = [
		"vehicles/",
		"modules/engines/",
		"modules/guns/",
		"modules/radios/",
		"modules/suspensions/",
		"modules/turrets/",
	]

	for d, base_dir in zip(ds, base_dirs):
		for file in os.listdir(base_dir):
			if file.startswith("."):
				continue
			for k, v in json.load(open(base_dir + file)).items():
				d[int(k)] = v

if __name__ == "__main__":
	load()
	# print(len(guns))

	for vehicle in vehicles.values():
		d = [
			vehicle["tier"],
			vehicle["nation"],
			vehicle["name"],
			vehicle["default_profile"]["hull_hp"],
			vehicle["default_profile"]["armor"]["hull"]["front"],
			vehicle["default_profile"]["armor"]["hull"]["sides"],
			vehicle["default_profile"]["armor"]["hull"]["rear"],
		]
		print(d)
		gs = [guns[gid] for gid in vehicle["guns"]]
		max_tier = max(g["tier"] for g in gs)
		max_tier_gs = [g for g in gs if g["tier"] == max_tier]

		for g in max_tier_gs:
			print(g["tier"], g["module_id"])
			l = [
				g["default_profile"]["gun"]["aim_time"],
				g["default_profile"]["gun"]["fire_rate"],
				g["default_profile"]["gun"]["move_down_arc"],
				g["default_profile"]["gun"]["move_up_arc"],
				g["default_profile"]["gun"]["reload_time"],
			]
			print(l)


