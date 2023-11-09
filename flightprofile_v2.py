# Flight Profile of a Rocket
# FP v2

# Importing necessary libraries
import math

# Setting up initials
mass_wet = 136
coef_drag = 0.373
cs_area = 0.0366
mass_dry = 80.531
area_reef = 7.331519195
area_main = 15.10334678
cht_cd = 2.2
dply_main = 400
lnch_alt = 1219
hgt_rail = 13.1064
temp_init = 34
t_step = 0.01

# Setting up variables
line = 0
t_cur = 0
altitude = 0
velocity = 0
accel = -9.81
f = open("propmass.txt")
propcont = f.readlines()
prop_mass = propcont[line]
f.close()
mass_cur = float(prop_mass) + mass_dry
weight = mass_cur * 9.81
drag = 0
f = open("thrust.txt")
thrucont = f.readlines()
thrust = thrucont[line]
f.close()
sum_force = float(thrust) - weight - drag
hgt_asl = lnch_alt + altitude
if hgt_asl < 11000:
	temp = -0.0092485 * hgt_asl + (temp_init + 11.2734)
else:
	temp = -56.46
if hgt_asl < 11000:
	air_pres = 101.29 * ((temp + 273.1) / 288.08)
else:
	air_pres = 22.65 * math.exp(1.73-(0.000157*hgt_asl))


print(prop_mass)
print(thrust)
