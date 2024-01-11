# Rocket Simulator Application
# v1.0

# Importing necessary libraries
from tkinter import *
from math import *

# Setting up tkinter window
root = Tk()
root.title("Rocket Simulator")
root.geometry("475x315")
root.configure(background="#404040")

# Taking input through tkinter window
title1 = Label(root, text="Enter time step (s)", fg="white", bg="#404040")
title1.grid(row=0, column=0)
e_tstep = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_tstep.grid(row=1, column=0, padx=10)

title2 = Label(root, text="Enter total propellant mass (kg)", fg="white", bg="#404040")
title2.grid(row=2, column=0)
e_propmass = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_propmass.grid(row=3, column=0, padx=10)

title3 = Label(root, text="Enter dry mass (kg)", fg="white", bg="#404040")
title3.grid(row=4, column=0)
e_drymass = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_drymass.grid(row=5, column=0, padx=10)

title4 = Label(root, text="Enter OF ratio", fg="white", bg="#404040")
title4.grid(row=6, column=0)
e_ofratio = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_ofratio.grid(row=7, column=0, padx=10)

title5 = Label(root, text="Enter average thrust (N)", fg="white", bg="#404040")
title5.grid(row=8, column=0)
e_avgthru = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_avgthru.grid(row=9, column=0, padx=10)

title6 = Label(root, text="Enter port radius (m)", fg="white", bg="#404040")
title6.grid(row=10, column=0)
e_radport = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_radport.grid(row=11, column=0, padx=10)

title7 = Label(root, text="Enter rocket cross-section (m^2)", fg="white", bg="#404040")
title7.grid(row=12, column=0)
e_csarea = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_csarea.grid(row=13, column=0, padx=10)

title8 = Label(root, text="Enter initial height ASL (m)", fg="white", bg="#404040")
title8.grid(row=14, column=0)
e_hgtasl = Entry(root, width=35, borderwidth=0, fg="white", bg="#636363")
e_hgtasl.grid(row=15, column=0, padx=10)


def clear():
    lst = root.place_slaves()
    for i in lst:
        i.destroy()


def rocksim():
    # Checking inputs
    # noinspection PyBroadException
    try:
        float(e_tstep.get())
        float(e_propmass.get())
        float(e_drymass.get())
        float(e_ofratio.get())
        float(e_avgthru.get())
        float(e_radport.get())
        float(e_csarea.get())
        float(e_hgtasl.get())
    except:
        Label(root, text="At least one field is invalid.", fg="red", bg="#404040").place(x=350, y=140, anchor="center")
        return None
    clear()
    Button(root, text="Launch rocket!", command=rocksim, fg="white", bg="#636363", borderwidth=0).place(x=350, y=30, anchor="center")

    # Motor Simulation

    # Setting up initials
    thrust_txt = []
    propmass_txt = []
    t_step = float(e_tstep.get())  # s
    rad_liner = 6.98 / (2 * 39.37)  # m
    mass_ox = float(e_propmass.get()) * (float(e_ofratio.get()) / (float(e_ofratio.get()) + 1))  # kg
    mass_fu = mass_ox / float(e_ofratio.get())  # kg
    avg_thrust = float(e_avgthru.get())  # N
    rad_port = float(e_radport.get())  # m
    area_port = pi * (rad_port ** 2)  # m^2
    isp = 200  # s
    grav = 9.81  # m/s^2
    eta_c = 0.95  # coef
    eta_n = 0.95  # coef
    mdot_ox = (avg_thrust / (isp * grav * eta_c * eta_n)) / (1 + (1 / float(e_ofratio.get())))  # kg/s
    a = 0.417  # const
    n = 0.347  # const
    rho_fuel = (0.871 * 901) + (0.129 * 1220)  # kg/m^3
    vol_grain = mass_fu / rho_fuel  # m^3
    hgt_grain = vol_grain / ((pi * (rad_liner ** 2)) - (pi * (rad_port ** 2)))  # m

    # Calculating first line
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
    thrust_txt.append(thrust)
    propmass_txt.append(prop_mass)

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
        thrust_txt.append(thrust)
        propmass_txt.append(prop_mass)
        if t_cur > mass_ox / mdot_ox:
            break

    # Rocket Simulation

    # Setting up initials
    mass_dry = float(e_drymass.get())
    cs_area = float(e_csarea.get())
    hgt_init = float(e_hgtasl.get())
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
            alt_lst.sort()
            vel_lst.sort()
            acc_lst.sort()
            alt_lbl = Label(root, text="Max altitude: " + str(round(alt_lst[-1], 3)) + " m", fg="white", bg="#404040")
            alt_lbl.place(x=350, y=60, anchor="center")
            vel_lbl = Label(root, text="Max velocity: " + str(round(vel_lst[-1], 3)) + " m/s", fg="white", bg="#404040")
            vel_lbl.place(x=350, y=80, anchor="center")
            acc_lbl = Label(root, text="Max acceleration: " + str(round(acc_lst[-1], 3)) + " m/s^2", fg="white", bg="#404040")
            acc_lbl.place(x=350, y=100, anchor="center")
            break


# The button
Button(root, text="Launch rocket!", command=rocksim, fg="white", bg="#636363", borderwidth=0).place(x=350, y=30, anchor="center")

# Displaying the tkinter window
root.mainloop()
