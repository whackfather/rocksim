# Rocket Simulator (No GUI)
# v1.0

# Importing necessary libraries
from math import *

# Motor Simulation

# Setting up initials
thrust_txt = []
propmass_txt = []
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
reg_coef = 0.417  # const
fit_coef = 0.347  # const
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
reg_rate = reg_coef * ((ox_flux / 10) ** fit_coef)
fuel_mdot = rho_fuel * surface_area * (reg_rate / 1000)
fuel_mass = mass_fu - (fuel_mdot * t_cur)
ox_mass = mass_ox - (mdot_ox * t_cur)
prop_mass = fuel_mass + ox_mass
if t_cur < (mass_ox / mdot_ox):
    thrust = (mdot_ox + fuel_mdot) * isp * grav * eta_c * eta_n
else:
    thrust = 0
thrust_txt.append(thrust)
propmass_txt.append(prop_mass)

# Main loop
while True:
    t_cur += t_step
    if t_cur < (mass_ox / mdot_ox):
        ox_flux = mdot_ox / port_area
    else:
        ox_flux = 0
    reg_rate = reg_coef * ((ox_flux / 10) ** fit_coef)
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
    thrust_txt.append(thrust)
    propmass_txt.append(prop_mass)
    if t_cur > mass_ox / mdot_ox:
        print("Motor simulation complete.")
        break

# Rocket Simulation

# Setting up initials
mass_dry = 70  # kg
cs_area = 0.0366  # m^2
hgt_init = 1219.2  # m
alt_lst = []
vel_lst = []
acc_lst = []
den_lst = []

# Calculating first line
line = 0
t_cur = 0
altitude = 0
alt_lst.append(altitude)
velocity = 0
vel_lst.append(velocity)
drag = 0
prop_mass = propmass_txt[line]
mass_cur = prop_mass + mass_dry
weight = mass_cur * grav
thrust = thrust_txt[line]
sum_force = thrust - weight - drag
accel = sum_force / mass_cur
acc_lst.append(accel)
hgt_asl = hgt_init + altitude
if hgt_asl < 11000:
    air_temp = -0.0092485 * hgt_asl + (33.95 + 11.2734)
    air_pres = 101.29 * (((air_temp + 273.15) / 288.08) ** 5.256)
else:
    air_temp = -56.46
    air_pres = 22.65 * (e ** (1.73 - (0.000157 * hgt_asl)))
air_den = air_pres / (0.2869 * (air_temp + 273.1))
den_lst.append(air_den)
spd_snd = sqrt((1.4 * 8.3145 * (air_temp + 273.15) / 0.028964))
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

# Main loop
while True:
    line += 1
    if line >= (len(thrust_txt) - 1):
        line = len(thrust_txt) - 1
    t_cur += t_step
    drag = (0.5 * Cd * cs_area * air_den * velocity * abs(velocity))
    prop_mass = propmass_txt[line]
    mass_cur = prop_mass + mass_dry
    weight = mass_cur * grav
    thrust = thrust_txt[line]
    sum_force = thrust - weight - drag
    ac_fut = sum_force / mass_cur
    ac_avg = (accel + ac_fut) / 2
    vel_fut = velocity + (ac_avg * t_step)
    vel_avg = (velocity + vel_fut) / 2
    altitude += (vel_avg * t_step)
    alt_lst.append(altitude)
    velocity = vel_fut
    vel_lst.append(velocity)
    accel = ac_fut
    acc_lst.append(accel)
    hgt_asl = hgt_init + altitude
    if hgt_asl < 11000:
        air_temp = -0.0092485 * hgt_asl + (33.95 + 11.2734)
        air_pres = 101.29 * (((air_temp + 273.15) / 288.08) ** 5.256)
    else:
        air_temp = -56.46
        air_pres = 22.65 * (e ** (1.73 - (0.000157 * hgt_asl)))
    air_den = air_pres / (0.2869 * (air_temp + 273.1))
    den_lst.append(air_den)
    spd_snd = sqrt((1.4 * 8.3145 * (air_temp + 273.15) / 0.028964))
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
        alt_lst.sort()
        vel_lst.sort()
        acc_lst.sort()
        print("Max altitude: " + str(round(alt_lst[-1], 3)) + " m")
        print("Max velocity: " + str(round(vel_lst[-1], 3)) + " m/s")
        print("Max acceleration: " + str(round(acc_lst[-1], 3)) + " m/s^2")
        break
