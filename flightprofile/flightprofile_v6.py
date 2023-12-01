# Flight Profile of a Rocket
# FP v6

# Importing necessary libraries
import math

# Fluff
print("Loading...")

# Setting up initials
coef_drag = 0.6
cs_area = 0.0366
mass_dry = 63.786
area_reef = 0.7974732057
area_main = 15.10334678
cht_cd = 2.2
dply_main = 400
lnch_alt = 1219
hgt_rail = 13.1064
temp_init = 34
t_step = 0.01
alt_lst = []
vel_lst = []
mach_lst = []

# Setting up first line
line = 0
t_cur = 0
altitude = 0
alt_lst.append(altitude)
velocity = 0
vel_lst.append(velocity)
accel = -9.81
f = open("propmass.txt")
propcont = f.readlines()
prop_mass = float(propcont[line])
f.close()
mass_cur = prop_mass + mass_dry
weight = mass_cur * 9.81
drag = 0
f = open("thrust.txt")
thrucont = f.readlines()
thrust = float(thrucont[line])
f.close()
sum_force = thrust - weight - drag
hgt_asl = lnch_alt + altitude
if hgt_asl < 11000:
	air_temp = -0.0092485 * hgt_asl + (temp_init + 11.2734)
	air_pres = 101.29 * ((air_temp + 273.1) / 288.08)
else:
	air_temp = -56.46
	air_pres = 22.65 * math.exp(1.73 - (0.000157 * hgt_asl))
air_den = air_pres / (0.2869 * (air_temp + 273.1))
spd_snd = 331.3 * math.sqrt(1 + (air_temp / 273.15))
mach_n = abs(velocity / spd_snd)
mach_lst.append(mach_n)
if mach_n <= 0.019892:
	Cd = (-0.25 * mach_n) + 0.6
elif 0.019892 < mach_n <= 0.08:
	Cd = (7.61905 * (mach_n ** 2)) - (1.65476 * mach_n) + 0.624929
elif 0.08 < mach_n <= 0.13:
	Cd = (-0.042 * mach_n) + 0.54466
elif 0.13 < mach_n <= 0.9129:
	Cd = 0.494437 * (mach_n ** -0.0424974)
elif 0.9129 < mach_n <= 1.0499712:
	Cd = (2.09956 * mach_n) - 1.42042
elif 1.0499712 < mach_n <= 1.4379:
	Cd = (0.54702 * (mach_n ** 2)) - (1.30393 * mach_n) + 1.55009
else:
	Cd = 0.951585 * (mach_n ** -0.456674)
g_load = abs(accel) / 9.81

# Setting up second line
line += 1
t_cur += t_step
drag = 0
f = open("propmass.txt")
propcont = f.readlines()
prop_mass = float(propcont[line])
f.close()
mass_cur = prop_mass + mass_dry
weight = mass_cur * 9.81
f = open("thrust.txt")
thrucont = f.readlines()
thrust = float(thrucont[line])
f.close()
sum_force = thrust - weight - drag
ac_fut = sum_force / mass_cur
ac_avg = (accel + ac_fut) / 2
velocity += (ac_avg * t_step)
vel_lst.append(velocity)
altitude += (velocity * t_step) + (0.5 * ac_avg * t_step * t_step)
alt_lst.append(altitude)
accel = ac_fut
hgt_asl = lnch_alt + altitude
if hgt_asl < 11000:
	air_temp = -0.0092485 * hgt_asl + (temp_init + 11.2734)
	air_pres = 101.29 * ((air_temp + 273.1) / 288.08)
else:
	air_temp = -56.46
	air_pres = 22.65 * math.exp(1.73 - (0.000157 * hgt_asl))
air_den = air_pres / (0.2869 * (air_temp + 273.1))
spd_snd = 331.3 * math.sqrt(1 + (air_temp / 273.15))
mach_n = abs(velocity / spd_snd)
mach_lst.append(mach_n)
if mach_n <= 0.019892:
	Cd = (-0.25 * mach_n) + 0.6
elif 0.019892 < mach_n <= 0.08:
	Cd = (7.61905 * (mach_n ** 2)) - (1.65476 * mach_n) + 0.624929
elif 0.08 < mach_n <= 0.13:
	Cd = (-0.042 * mach_n) + 0.54466
elif 0.13 < mach_n <= 0.9129:
	Cd = 0.494437 * (mach_n ** -0.0424974)
elif 0.9129 < mach_n <= 1.0499712:
	Cd = (2.09956 * mach_n) - 1.42042
elif 1.0499712 < mach_n <= 1.4379:
	Cd = (0.54702 * (mach_n ** 2)) - (1.30393 * mach_n) + 1.55009
else:
	Cd = 0.951585 * (mach_n ** -0.456674)
g_load = abs(accel) / 9.81

# Main loop, lines 3 and beyond
while True:
	line += 1
	# Set "1516" to the last line of data in thrust.txt minus one
	# i.e. the last line of data in our thrust.txt is 1517, so we use 1516 here
	if line >= 1367:
		line = 1367
	t_cur += t_step
	if abs(velocity) / velocity == -1 and altitude <= dply_main:
		drag = (0.5 * cht_cd * area_main * air_den * velocity * abs(velocity))
		x = 1
	elif abs(velocity) / velocity == -1:
		drag = (0.5 * cht_cd * area_reef * air_den * velocity * abs(velocity))
		x = 2
	else:
		drag = (0.5 * Cd * cs_area * air_den * velocity * abs(velocity))
		x = 3
	f = open("propmass.txt")
	propcont = f.readlines()
	prop_mass = float(propcont[line])
	f.close()
	mass_cur = prop_mass + mass_dry
	weight = mass_cur * 9.81
	f = open("thrust.txt")
	thrucont = f.readlines()
	thrust = float(thrucont[line])
	f.close()
	sum_force = thrust - weight - drag
	ac_fut = sum_force / mass_cur
	ac_avg = (accel + ac_fut) / 2
	velocity += (ac_avg * t_step)
	vel_lst.append(velocity)
	altitude += (velocity * t_step) + (0.5 * ac_avg * t_step * t_step)
	alt_lst.append(altitude)
	accel = ac_fut
	hgt_asl = lnch_alt + altitude
	if hgt_asl < 11000:
		air_temp = -0.0092485 * hgt_asl + (temp_init + 11.2734)
		air_pres = 101.29 * ((air_temp + 273.1) / 288.08)
	else:
		air_temp = -56.46
		air_pres = 22.65 * math.exp(1.73 - (0.000157 * hgt_asl))
	air_den = air_pres / (0.2869 * (air_temp + 273.1))
	spd_snd = 331.3 * math.sqrt(1 + (air_temp / 273.15))
	mach_n = abs(velocity / spd_snd)
	mach_lst.append(mach_n)
	if mach_n <= 0.019892:
		Cd = (-0.25 * mach_n) + 0.6
	elif 0.019892 < mach_n <= 0.08:
		Cd = (7.61905 * (mach_n ** 2)) - (1.65476 * mach_n) + 0.624929
	elif 0.08 < mach_n <= 0.13:
		Cd = (-0.042 * mach_n) + 0.54466
	elif 0.13 < mach_n <= 0.9129:
		Cd = 0.494437 * (mach_n ** -0.0424974)
	elif 0.9129 < mach_n <= 1.0499712:
		Cd = (2.09956 * mach_n) - 1.42042
	elif 1.0499712 < mach_n <= 1.4379:
		Cd = (0.54702 * (mach_n ** 2)) - (1.30393 * mach_n) + 1.55009
	else:
		Cd = 0.951585 * (mach_n ** -0.456674)
	g_load = abs(accel) / 9.81
	if velocity < 0:
		alt_lst.sort()
		vel_lst.sort()
		mach_lst.sort()
		print("Max altitude: " + str(round(alt_lst[-1], 3)) + " m")
		print("Max velocity: " + str(round(vel_lst[-1], 3)) + " m/s")
		print("Max mach: " + str(round(mach_lst[-1], 3)))
		print("Simulation complete.")
		exit(0)