# Flight Profile of a Rocket
# FP v4

# Importing necessary libraries
import math

# Fluff
print("Loading...")

# Setting up initials
coef_drag = 0.373
cs_area = 0.0366
mass_dry = 54.638
area_reef = 0.7974732057
area_main = 15.10334678
cht_cd = 2.2
dply_main = 400
lnch_alt = 1219
hgt_rail = 13.1064
temp_init = 34
t_step = 0.01
alt_lst = []

# Setting up first line
line = 0
t_cur = 0
altitude = 0
alt_lst.append(altitude)
velocity = 0
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
if mach_n < 0.09:
	Cd = (-0.879762 * mach_n) + 0.393714
elif 0.09 <= mach_n < 0.12:
	Cd = 0.327
elif 0.12 <= mach_n < 0.38:
	Cd = (-0.0952479 * mach_n) + 0.33672
elif 0.38 <= mach_n < 0.56:
	Cd = (-0.0513932 * mach_n) + 0.321231
elif 0.56 <= mach_n < 0.62:
	Cd = 0.293
elif 0.62 <= mach_n < 0.91:
	Cd = (0.0260591 * mach_n) + 0.277505
elif 0.91 <= mach_n < 1.06:
	Cd = (0.809643 * mach_n) - 0.434983
elif 1.06 <= mach_n < 1.12:
	Cd = (-0.06 * mach_n) + 0.477267
elif 1.12 <= mach_n < 1.23:
	Cd = 0.41
elif 1.23 <= mach_n < 1.41:
	Cd = (0.435648 * (mach_n ** 2)) - (1.01596 * mach_n) + 1.00167
elif 1.41 <= mach_n < 1.61:
	Cd = (-0.218947 * mach_n) + 0.744616
elif 1.61 <= mach_n < 2.01:
	Cd = (-0.164103 * mach_n) + 0.655777
elif 2.01 <= mach_n < 2.47:
	Cd = (-0.111765 * mach_n) + 0.551169
else:
	Cd = (-0.0815523 * mach_n) + 0.477042
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
if mach_n < 0.09:
	Cd = (-0.879762 * mach_n) + 0.393714
elif 0.09 <= mach_n < 0.12:
	Cd = 0.327
elif 0.12 <= mach_n < 0.38:
	Cd = (-0.0952479 * mach_n) + 0.33672
elif 0.38 <= mach_n < 0.56:
	Cd = (-0.0513932 * mach_n) + 0.321231
elif 0.56 <= mach_n < 0.62:
	Cd = 0.293
elif 0.62 <= mach_n < 0.91:
	Cd = (0.0260591 * mach_n) + 0.277505
elif 0.91 <= mach_n < 1.06:
	Cd = (0.809643 * mach_n) - 0.434983
elif 1.06 <= mach_n < 1.12:
	Cd = (-0.06 * mach_n) + 0.477267
elif 1.12 <= mach_n < 1.23:
	Cd = 0.41
elif 1.23 <= mach_n < 1.41:
	Cd = (0.435648 * (mach_n ** 2)) - (1.01596 * mach_n) + 1.00167
elif 1.41 <= mach_n < 1.61:
	Cd = (-0.218947 * mach_n) + 0.744616
elif 1.61 <= mach_n < 2.01:
	Cd = (-0.164103 * mach_n) + 0.655777
elif 2.01 <= mach_n < 2.47:
	Cd = (-0.111765 * mach_n) + 0.551169
else:
	Cd = (-0.0815523 * mach_n) + 0.477042
g_load = abs(accel) / 9.81

# Main loop, lines 3 and beyond
while True:
	line += 1
	if line >= 1400:
		line = 1400
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
	if mach_n < 0.09:
		Cd = (-0.879762 * mach_n) + 0.393714
	elif 0.09 <= mach_n < 0.12:
		Cd = 0.327
	elif 0.12 <= mach_n < 0.38:
		Cd = (-0.0952479 * mach_n) + 0.33672
	elif 0.38 <= mach_n < 0.56:
		Cd = (-0.0513932 * mach_n) + 0.321231
	elif 0.56 <= mach_n < 0.62:
		Cd = 0.293
	elif 0.62 <= mach_n < 0.91:
		Cd = (0.0260591 * mach_n) + 0.277505
	elif 0.91 <= mach_n < 1.06:
		Cd = (0.809643 * mach_n) - 0.434983
	elif 1.06 <= mach_n < 1.12:
		Cd = (-0.06 * mach_n) + 0.477267
	elif 1.12 <= mach_n < 1.23:
		Cd = 0.41
	elif 1.23 <= mach_n < 1.41:
		Cd = (0.435648 * (mach_n ** 2)) - (1.01596 * mach_n) + 1.00167
	elif 1.41 <= mach_n < 1.61:
		Cd = (-0.218947 * mach_n) + 0.744616
	elif 1.61 <= mach_n < 2.01:
		Cd = (-0.164103 * mach_n) + 0.655777
	elif 2.01 <= mach_n < 2.47:
		Cd = (-0.111765 * mach_n) + 0.551169
	else:
		Cd = (-0.0815523 * mach_n) + 0.477042
	g_load = abs(accel) / 9.81
	if velocity < 0:
		alt_lst.sort()
		print("Max altitude: " + str(round(alt_lst[-1], 3)) + " m")
		print("Simulation complete.")
		exit(0)
