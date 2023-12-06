# Flight Profile
# v2.1

# Importing necessary libraries
import math

# Fluff
from time import sleep
print("Launching rocket...")

# Setting up initials
isp = 180  # s
mass_dry = 70  # kg
grav = 9.81  # m/s^2
t_step = 0.01  # s
cs_area = 0.0366  # m^2
hgt_init = 1219.2  # m
alt_lst = []

# Setting up variables
line = 0
t_cur = 0
altitude = 0
alt_lst.append(altitude)
velocity = 0
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
accel = sum_force / mass_cur
hgt_asl = hgt_init + altitude
if hgt_asl < 11000:
	air_temp = 26.85 + (15.01 - (0.00649 * hgt_asl))
	air_pres = 101.29 * (((air_temp + 273.15) / 288.08) ** 5.256)
else:
	air_temp = 26.85 - 56.46
	air_pres = 22.65 ** (1.73 - (0.000157 * hgt_asl))
air_den = air_pres / (0.2869 * (air_temp + 273.1))
spd_snd = math.sqrt((1.4 * 8.3145 * (air_temp + 273.15) / 0.028964))
mach_n = abs(velocity / spd_snd)
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

while True:
	line += 1
	if line >= 2301:
		line = 2301
	t_cur += t_step
	drag = (0.5 * Cd * cs_area * air_den * velocity * abs(velocity))
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
	hgt_asl = hgt_init + altitude
	if hgt_asl < 11000:
		air_temp = 26.85 + (15.01 - (0.00649 * hgt_asl))
		air_pres = 101.29 * (((air_temp + 273.15) / 288.08) ** 5.256)
	else:
		air_temp = 26.85 - 56.46
		air_pres = 22.65 ** (1.73 - (0.000157 * hgt_asl))
	air_den = air_pres / (0.2869 * (air_temp + 273.1))
	spd_snd = math.sqrt((1.4 * 8.3145 * (air_temp + 273.15) / 0.028964))
	mach_n = abs(velocity / spd_snd)
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
	if velocity < 0:
		print("Finalizing data...")
		sleep(2)
		alt_lst.sort()
		print("Max altitude: " + str(round(alt_lst[-1], 3)) + " m")
		sleep(0.5)
		print("Simulation complete.")
		sleep(0.2)
		exit(0)
