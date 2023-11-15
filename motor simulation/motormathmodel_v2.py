# Flight Profile of a Rocket
# Motor Math Model v2

# Importing necessary libraries
from math import pi

# Setting up initials
t_step = 0.01  # s
mass_ox = 48.07333124  # kg
mass_fu = 15.8663  # kg
p_tank = 5516000  # pa
thrust_avg = 7000  # N
rad_port = 0.063  # m
a_port = pi * (rad_port ** 2)  # m^2
isp = 180  # s
grav = 9.81  # m/s^2
mdot_ox = (thrust_avg / (isp * grav)) / (1 + (1 / 6.5))  # kg/s
hgt_fu = 1.07553898867  # m
rho_fu = (0.871 * 901) + (0.129 * 1220)  # kg/m^3
burn_time = 13.99  # s
a = 0.417  # const
n = 0.347  # const

# Setting up variables
t_cur = 0
port_area = a_port
port_radius = rad_port
surface_area = 2 * pi * port_radius * hgt_fu
if t_cur < (mass_ox / mdot_ox):
	ox_flux = mdot_ox / a_port
else:
	ox_flux = 0
reg_rate = a * ((ox_flux / 10) ** n)
fuel_mdot = rho_fu * surface_area * (reg_rate / 1000)
fuel_mass = mass_fu - (fuel_mdot * t_cur)
ox_mass = mass_ox - (mdot_ox * t_cur)
prop_mass = fuel_mass + ox_mass
if t_cur < (mass_ox / mdot_ox):
	thrust = (mdot_ox + fuel_mdot) * isp * grav
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
	surface_area = 2 * pi * port_radius * hgt_fu
	fuel_mdot = rho_fu * surface_area * (reg_rate / 1000)
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
		thrust = (mdot_ox + fuel_mdot) * isp * grav
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
	if t_cur >= 13.99:
		print("Simulation complete.")
		print("Check thrust.txt and propmass.txt to verify calculations.")
		exit(0)
