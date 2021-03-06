# coding: utf-8

import json
import os
import copy
import gettext

class Gun:
	def __init__(self, reload_time):
		self.reload_time = reload_time
		self.is_autoloader = False
		self.clip_count = -1
		self.clip_rate = -1
		self.shells = []

class Turret:
	def __init__(self, health, view, front, sides, rear):
		self.health = health
		self.view = view
		self.front = front
		self.sides = sides
		self.rear = rear
		self.guns = []

class Vehicle:
	def __init__(self, contry, tunk_type, level, name):
		self.contry = contry
		self.tunk_type = tunk_type
		self.level = level

		f, n = name[1:].split(":")

		_ = gettext.translation(
			domain=f,
			localedir='locale',
			languages=["ja"]).gettext

		self.name = _(n)
		self.health = -1
		self.front = -1
		self.sides = -1
		self.rear = -1
		self.turrets = []

	def __str__(self):
		return self.name

	def line(self):
		ol = [
			self.contry,
			self.tunk_type,
			str(self.level),
			self.name,
			self.health,
			str(self.front),
			str(self.sides),
			str(self.rear),
			str(self.still),
			str(self.moving),
		]
		for turret in self.turrets:
			tl = copy.deepcopy(ol)
			tl[4] = str(tl[4] + turret.health)

			l = [
				str(turret.view),
				"-" if turret.front < 0 else str(turret.front),
				"-" if turret.sides < 0 else str(turret.sides),
				"-" if turret.rear < 0 else str(turret.rear),
			]
			tl += l
			for gun in turret.guns:
				gl = copy.deepcopy(tl)
				l = [
					str(int(gun.reload_time*10)/10.),
					"-" if gun.clip_count < 0 else str(gun.clip_count),
					"-" if gun.clip_rate < 0 else str(gun.clip_rate),
				]

				for shell in gun.shells:
					l.append(shell["kind"])
					l.append(str(shell["p100"]))
					l.append(str(shell["p500"]))
					l.append(str(shell["caliber"]))
					l.append(str(shell["speed"]))
					l.append(str(shell["damage"]))

				for i in range(3 - len(gun.shells)):
					l.append("-")
					l.append("-")
					l.append("-")
					l.append("-")
					l.append("-")
					l.append("-")

				gl += l

				print("\t".join(gl))

def shell_detail(sjson):
	d = {}
	d["damage"] = sjson["damage"]["armor"]
	d["caliber"] = float(sjson["caliber"])
	kindd = {
		"ARMOR_PIERCING":"AP",
		"ARMOR_PIERCING_CR":"APCR",
		"HIGH_EXPLOSIVE":"HE",
		"HOLLOW_CHARGE":"HEAT"
	}
	d["kind"] = kindd[sjson["kind"]]
	d["price"] = sjson["price"]

	return d

def gun_detail(gjson):
	# Bug?? incorrect?
	reload_time = float(gjson["reloadTime"])
	gun = Gun(reload_time)

	# rotationSpeed
	# turretYawLimits
	
	# FV206?
	if isinstance(gjson["shots"], unicode):
		return gun

	for shootk, shootv in gjson["shots"].items():
		shell = shell_detail(shell_json[shootk])
		
		p100, p500 = shootv["piercingPower"].split()
		shell["p100"] = float(p100)
		shell["p500"] = float(p500)

		shell["speed"] = shootv["speed"]
		gun.shells.append(shell)

	d = {
		"AP":1,
		"APCR":2,
		"HEAT":3,
		"HE":4,
	}

	gun.shells.sort(key=lambda s: (d[s["kind"]], s["p100"]))

	if "clip"in gjson:
		# auto loader
		gun.is_autoloader = True
		gun.clip_count = gjson["clip"]["count"]
		gun.clip_rate = gjson["clip"]["rate"]

	return gun

def vehicle_detail(vehicle, vjson, tunk_type):
	front, sides, rear =  vjson["hull"]["primaryArmor"].split()
	armor = vjson["hull"]["armor"]
	
	vehicle.health = vjson["hull"]["maxHealth"]
	vehicle.front = armor[front]
	vehicle.sides = armor[sides]
	vehicle.rear = armor[rear]
	vehicle.still = float(vjson["invisibility"]["still"])
	vehicle.moving = float(vjson["invisibility"]["moving"])
	vehicle.fire_penalty = float(vjson["invisibility"]["firePenalty"])

	turrets = vjson["turrets0"]
	# if turrets is None:
	# 	# Obserer?
	# 	return

	unleaf_guns = []
	unleaf_turrets = []
	max_gun_level = 0
	max_turret_level = 0

	for turretk, turret in turrets.items():
		max_turret_level = max(max_turret_level, turret["level"])
		
		for gunk, gunv in turret["guns"].items():
			level = guns_json["shared"][gunk]["level"]
			max_gun_level = max(max_gun_level, level)
		
			if "unlocks" in gunv:
				if "gun" in gunv["unlocks"]:
					unleaf_guns.append(gunk)

		if "unlocks" in turret:
			if "turret" in turret["unlocks"]:
				unleaf_turrets.append(turretk)

	for turretk, turret in turrets.items():
		if turretk in unleaf_turrets or turret["level"] != max_turret_level:
			continue

		health = turret["maxHealth"]
		view = turret["circularVisionRadius"]	
		
		if tunk_type not in ("SPG", "TD") and "primaryArmor" in turret:
			front, sides, rear = turret["primaryArmor"].split()
			
			front = turret["armor"][front]
			sides = turret["armor"][sides]
			rear = turret["armor"][rear]
			vturret = Turret(health, view, front, sides, rear)
		else:
			vturret = Turret(health, view, -1, -1, -1)
		
		for gunk, gunv in turret["guns"].items():
			if gunk in unleaf_guns or guns_json["shared"][gunk]["level"] != max_gun_level:
				continue
			
			vgun = gun_detail(guns_json["shared"][gunk])
			
			if "reloadTime" in turret:
				vgun.reload_time = float(gunv["reloadTime"])

			vturret.guns.append(vgun)

		vehicle.turrets.append(vturret)

if __name__ == "__main__":
	l = [
		"country",
		"type",
		"tier",
		"name",
		"HP",
		"front",
		"sides",
		"rear",
		"still",
		"moving",
		"view",
		"tfront",
		"tsides",
		"trear",
		"reload",
		"clip_count",
		"clip_rate",
		"shell1_type",
		"shell1_p100",
		"shell1_p500",
		"shell1_speed",
		"shell1_caliber",
		"shell1_damage",
		"shell2_type",
		"shell2_p100",
		"shell2_p500",
		"shell2_speed",
		"shell2_caliber",
		"shell2_damage",
		"shell3_type",
		"shell3_p100",
		"shell3_p500",
		"shell3_speed",
		"shell3_caliber",
		"shell3_damage",
	]
	print("\t".join(l))

	base_dir = "vehicles"
	for d in os.listdir(base_dir):
		if not os.path.isdir(os.path.join(base_dir, d)):
			continue

		if d == "common":
			continue

		global guns_json
		global shells_json

		guns_json = json.load(open(os.path.join(base_dir, d, 'components', 'guns.json')))
		shell_json = json.load(open(os.path.join(base_dir, d, 'components', 'shells.json')))

		list_json = json.load(open(os.path.join(base_dir, d, "list.json")))
		
		for vk, vv in list_json.items():
			tags = vv["tags"].split()
			if "secret" in tags:
				continue

			td = {
				"heavyTank":"HT",
				"AT-SPG":"TD",
				"mediumTank":"MT",
				"lightTank":"LT",
				"SPG":"SPG"
			}
			tk = ""
			for v in tags:
				if v in td:
					tk = td[v]

			vehicle = Vehicle(d, tk, vv["level"], vv["userString"])
			vjson = json.load(open(os.path.join(base_dir, d, vk + ".json")))
			vehicle_detail(vehicle, vjson, tk)

			vehicle.line()
			