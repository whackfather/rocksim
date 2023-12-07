# Motor Model
# v2.1

# Importing necessary libraries
from math import pi

# Fluff
print("Firing test motor...")

# Setting up initials
t_step = 0.01  # s
rad_liner = 6.98 / (2 * 39.37)  # m
mass_ox = 70 * (6.5 / 7.5)  # kg
mass_fu = mass_ox / 6.5  # kg
pres_tank = 5516000  # pa
avg_thrust = 5374.173913043480  # N
rad_port = 0.0544  # m
area_port = pi * (rad_port ** 2)  # m^2
isp = 200  # s
grav = 9.81  # m/s^2
eta_c = 0.95  # coef
eta_n = 0.95  # coef
mdot_ox = (avg_thrust / (isp * grav * eta_c * eta_n)) / (1 + (1 / 6.5))  # kg/s
a = 0.417  # const
n = 0.347  # const
rho_fuel = (0.871 * 901) + (0.129 * 1220)  # kg/m^3
vol_grain = mass_fu / rho_fuel  # m^3
hgt_grain = vol_grain / ((pi * (rad_liner ** 2)) - (pi * (rad_port ** 2)))  # m

# Setting up variables
t_cur = 0
port_area = area_port
port_radius = rad_port
surface_area = 2 * pi * port_radius * hgt_grain
if t_cur < (mass_ox / mdot_ox):
	ox_flux = mdot_ox / area_port
else:
	ox_flux = 0
reg_rate = a * ((ox_flux / 10) ** n)
fuel_mdot = rho_fuel * surface_area * (reg_rate / 1000)
fuel_mass = mass_fu - (fuel_mdot * t_cur)
ox_mass = mass_ox - (mdot_ox * t_cur)
prop_mass = fuel_mass + ox_mass
if t_cur < (mass_ox / mdot_ox):
	thrust = (mdot_ox + fuel_mdot) * isp * grav * eta_c * eta_n
else:
	thrust = 0

# Writing first thrust line
f = open("thrust.txt", "w")
f.write(str(thrust))
f.write("\n")
f.close()
f = open("propmass.txt", "w")
f.write(str(prop_mass))
f.write("\n")
f.close()

# Main loop
while True:
	t_cur += t_step
	if t_cur < (mass_ox / mdot_ox):
		ox_flux = mdot_ox / port_area
	else:
		ox_flux = 0
	reg_rate = a * ((ox_flux / 10) ** n)
	port_radius += ((reg_rate / 1000) * t_step)
	port_area = pi * (port_radius ** 2)
	surface_area = 2 * pi * port_radius * hgt_grain
	fuel_mdot = rho_fuel * surface_area * (reg_rate / 1000)
	if mass_fu - (fuel_mdot * t_cur) > fuel_mass:
		fuel_mass = fuel_mass
	else:
		fuel_mass = mass_fu - (fuel_mdot * t_cur)
	if mass_ox - (mdot_ox * t_cur) < 0:
		ox_mass = 0
	else:
		ox_mass = mass_ox - (mdot_ox * t_cur)
	prop_mass = fuel_mass + ox_mass
	if t_cur < (mass_ox / mdot_ox):
		thrust = (mdot_ox + fuel_mdot) * isp * grav * eta_c * eta_n
	else:
		thrust = 0
	f = open("thrust.txt", "a")
	f.write(str(thrust))
	f.write("\n")
	f.close()
	f = open("propmass.txt", "a")
	f.write(str(prop_mass))
	f.write("\n")
	f.close()
	if t_cur > mass_ox / mdot_ox:
		print("Simulation complete.")
		print("Check thrust.txt and propmass.txt to verify calculations.")
		print("Check thrust.txt for the final line number (important for use in main program).")
		exit(0)
