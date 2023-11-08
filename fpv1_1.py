# Flight Profile of a Rocket
# v1.1

# Importing necessary libraries
import math

# Setting up initials
t_init = 0  # Don't change this
t_step = 0.01  # s
hgt_init = 1  # m
cht_dply = 500  # m
v_init = 0  # m/s
grav = -9.81  # m/s^2
mass = 6.9  # kg
cd_rkt = 0.3  # coef
cd_cht = 2.3  # coef
cht_diam = 1.829  # m
drogue_diam = 0.203  # m
rkt_diam = 0.102  # m
pi = math.pi  # const
cs_rkt = pi * ((rkt_diam / 2) ** 2)  # m^2
cs_cht = pi * ((cht_diam / 2) ** 2)  # m^2
cs_drg = pi * ((drogue_diam / 2) ** 2)  # m^2
weight = grav * mass  # N
air_den = 1.225  # kg/m^3
alt_lst = []
vel_lst = []
tim_lst = []

# Setting up variables
t_cur = t_init
v_cur = v_init
hgt_cur = hgt_init
ac_cur = grav

# Main calculations loop
while True:
	# Defining chute drag
	if hgt_cur <= cht_dply and t_cur > 10:
		f_drag = (0.5 * air_den * -v_cur * abs(v_cur) * cd_cht * cs_cht)
	elif v_cur < 0:
		f_drag = (0.5 * air_den * -v_cur * abs(v_cur) * cd_cht * cs_drg)
	elif hgt_cur > cht_dply or t_cur < 10:
		f_drag = (0.5 * air_den * -v_cur * abs(v_cur) * cd_rkt * cs_rkt)

	# Progressing time
	t_cur += t_step

	# Defining thrust and its duration
	if t_cur < 5.5:
		f_thrust = 550
	else:
		f_thrust = 0

	# Calculating updated values
	f_net = f_thrust + weight + f_drag
	ac_fut = f_net / mass
	ac_act = (ac_cur + ac_fut) / 2
	ac_cur = ac_fut
	hgt_cur += (v_cur * t_step) + (0.5 * ac_act * t_step * t_step)
	v_cur += ac_act * t_step

	# Defining stopping condition or printing values
	if hgt_cur < 0:
		alt_lst.sort()
		vel_lst.sort()
		print("Max Altitude: " + str(round(alt_lst[-1], 3)) + " m")
		print("Max Velocity: " + str(round(vel_lst[-1], 3)) + " m/s")
		print("Time to Apogee: " + str(round(tim_lst[-1], 3)) + " s")
		print("Time in Flight: " + str(round(t_cur, 3)) + " s")
		print("Simulation complete.")
		exit(0)
	else:
		alt_lst.append(hgt_cur)
		vel_lst.append(v_cur)
		if abs(v_cur)/v_cur == 1:
			tim_lst.append(t_cur)
