import xml.etree.ElementTree as ET
import os
import copy

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
		self.name = name.split(":")[1]
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
					l.append(str(shell["damage"]))

				for i in range(3 - len(gun.shells)):
					l.append("-")
					l.append("-")
					l.append("-")

				gl += l

				print(", ".join(gl))

def shell_detail(sroot):
	d = {}
	d["damage"] = int(sroot.find("damage").find("armor").text)
	d["caliber"] = float(sroot.find("caliber").text)
	kindd = {
		"ARMOR_PIERCING":"AP",
		"ARMOR_PIERCING_CR":"APCR",
		"HIGH_EXPLOSIVE":"HE",
		"HOLLOW_CHARGE":"HEAT"
	}
	d["kind"] = kindd[sroot.find("kind").text]

	return d

def gun_detail(groot):
	# Bug?? incorrect?
	reload_time = float(groot.find("reloadTime").text)
	gun = Gun(reload_time)

	# rotationSpeed
	# turretYawLimits
	
	for shoot in groot.find("shots"):
		shell = shell_detail(shell_root.find(shoot.tag))
		
		p100, p500 = shoot.find("piercingPower").text.split()
		shell["p100"] = float(p100)
		shell["p500"] = float(p500)

		shell["speed"] = int(shoot.find("speed").text)
		gun.shells.append(shell)

	if groot.find("clip") is not None:
		# auto loader
		gun.is_autoloader = True
		gun.clip_count = int(groot.find("clip").find("count").text)
		gun.clip_rate = int(groot.find("clip").find("rate").text)

	return gun

def vehicle_detail(vehicle, vroot, groot, tunk_type):
	hull = vroot.find("hull")
	front, sides, rear = hull.find("primaryArmor").text.split()
	armor = hull.find("armor")
	health = int(hull.find("maxHealth").text)

	front = float(armor.find(front).text)
	sides = float(armor.find(sides).text)
	rear = float(armor.find(rear).text)

	vehicle.health = health
	vehicle.front = front
	vehicle.sides = sides
	vehicle.rear = rear

	turrets = vroot.find("turrets0")
	if turrets is None:
		# Obserer?
		return

	unleaf_guns = []
	unleaf_turrets = []
	max_gun_level = 0
	max_turret_level = 0

	for turret in turrets:
		level = int(float(turret.find("level").text))
		max_turret_level = max(max_turret_level, level)
				

		for gun in turret.find("guns"):
			level = int(groot.find("shared").find(gun.tag).find("level").text)
			max_gun_level = max(max_gun_level, level)
		
			unlocks = gun.findall("unlocks")
			if len(unlocks) != 0:
				unlock = unlocks[0]
				if len(unlock.findall("gun")) != 0:
					unleaf_guns.append(gun.tag)

		unlocks = turret.findall("unlocks")
		if len(unlocks) != 0:
			unlock = unlocks[0]
			if len(unlock.findall("turret")) != 0:
				unleaf_turrets.append(turret.tag)



	for turret in turrets:
		if turret.tag in unleaf_turrets or int(float(turret.find("level").text)) != max_turret_level:
			continue

		# level = int(turret.find("level").text)
		# print(level)
		health = float(turret.find("maxHealth").text)
		view = float(turret.find("circularVisionRadius").text)
		vturret = Turret(health, view, -1, -1, -1)
		parmor = turret.find("primaryArmor")
		
		if tunk_type not in ("SPG", "TD") and parmor is not None:
			front, sides, rear = parmor.text.split()
			armor = turret.find("armor")

			front = float(armor.find(front).text)
			sides = float(armor.find(sides).text)
			rear = float(armor.find(rear).text)
			vturret = Turret(health, view, front, sides, rear)

		
		for gun in turret.find("guns"):
			if gun.tag in unleaf_guns or int(groot.find("shared").find(gun.tag).find("level").text) != max_gun_level:
				continue
			
			vgun = gun_detail(groot.find("shared").find(gun.tag))
			
			if gun.find("reloadTime") is not None:
				vgun.read_time = float(gun.find("reloadTime").text)

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
		"view",
		"tfront",
		"tsides",
		"trear",
		"reload",
		"clip_count",
		"clip_rate",
		"shell1_type",
		"shell1_pierce",
		"shell1_damage",
		"shell2_type",
		"shell2_pierce",
		"shell2_damage",
		"shell3_type",
		"shell3_pierce",
		"shell3_damage",
	]
	print(", ".join(l))

	base_dir = "vehicles"
	for d in os.listdir(base_dir):
		if not os.path.isdir(os.path.join(base_dir, d)):
			continue

		if d == "common":
			continue

		global guns_root
		global shell_root

		guns_root = ET.parse(os.path.join(base_dir, d, 'components', 'guns.xml')).getroot()
		shell_root = ET.parse(os.path.join(base_dir, d, 'components', 'shells.xml')).getroot()

		list_xml = os.path.join(base_dir, d, "list.xml")
		list_root = ET.parse(list_xml).getroot()

		for child in list_root:
			tags = child.find("tags").text.split()
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

			vehicle = Vehicle(d, tk, int(child.find("level").text), child.find("userString").text)

			vroot = ET.parse(os.path.join(base_dir, d, child.tag.lower() + ".xml")).getroot()
			vehicle_detail(vehicle, vroot, guns_root, tk)

			# print(sum([len(t.guns) for t in vehicle.turrets]))
			vehicle.line()
			