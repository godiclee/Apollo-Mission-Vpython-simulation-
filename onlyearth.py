from vpython import *
from lol import *

# Information of different stages of rocket (From Saturn V)
Rocket_mass = [130000,40100,13500]  # Unit: kg (start from lowest stage to highest stage)
Fuel_mass   = [2290000-130000,496200-40100,123000-13500] # Gross mass - Empty mass
Thrust      = [3.51E7,5.14E6,1E6]
Burn_time   = [168,360,500]

# Create different stages of rocket
rocket1   = Rocket(Rocket_mass[0],Fuel_mass[0],Thrust[0],Burn_time[0],stage=1)
rocket2   = Rocket(Rocket_mass[1],Fuel_mass[1],Thrust[1],Burn_time[1],stage=2)
rocket3   = Rocket(Rocket_mass[2],Fuel_mass[2],Thrust[2],Burn_time[2],stage=3)
rocket23  = Rocket(stage='2+3')
rocket    = Rocket(stage='all')

rocket1L  = Rocket(stage='1L')
rocket2L  = Rocket(stage='2L')
rocket3L  = Rocket(stage='3L')
rocket23L = Rocket(stage='2+3L')
rocketL   = Rocket(stage='allL')

# Draw graphs
curve1 = graph(title ='h-t'    ,xtitle='time',ytitle='height'                   ,width=300,height=300,align='none')
curve2 = graph(title ='v-t'    ,xtitle='time',ytitle='velocity'            		,width=300,height=300,align='none')
curve3 = graph(title ='a-t'    ,xtitle='time',ytitle='acceleration'        		,width=300,height=300,align='none')
curve4 = graph(title ='angle-t',xtitle='time',ytitle='angle'                    ,width=300,height=300,align='none')
curve5 = graph(title ='g-t'    ,xtitle='time',ytitle='gravitional acceleration' ,width=300,height=300,align='none')
curve6 = graph(title ='d-t'    ,xtitle='time',ytitle='drag force'          		,width=300,height=300,align='none')
curve7 = graph(title ='m-t'    ,xtitle='time',ytitle='fuel_mass'                ,width=300,height=300,align='none')

height_curve1 = gcurve(color=color.blue,  graph=curve1)
height_curve2 = gcurve(color=color.green, graph=curve1)
height_curve3 = gcurve(color=color.red,   graph=curve1)
v_curve1      = gcurve(color=color.blue,  graph=curve2)
v_curve2      = gcurve(color=color.green, graph=curve2)
v_curve3      = gcurve(color=color.red,   graph=curve2)
a_curve1      = gcurve(color=color.blue,  graph=curve3)
a_curve2      = gcurve(color=color.green, graph=curve3)
a_curve3      = gcurve(color=color.red,   graph=curve3)
angle_curve1  = gcurve(color=color.blue,  graph=curve4)
angle_curve2  = gcurve(color=color.green, graph=curve4)
angle_curve3  = gcurve(color=color.red,   graph=curve4)
g_curve1      = gcurve(color=color.blue,  graph=curve5)
g_curve2      = gcurve(color=color.green, graph=curve5)
g_curve3      = gcurve(color=color.red,   graph=curve5)
d_curve1      = gcurve(color=color.blue,  graph=curve6)
d_curve2      = gcurve(color=color.green, graph=curve6)
d_curve3      = gcurve(color=color.red,   graph=curve6)
m_curve1      = gcurve(color=color.blue,  graph=curve7)
m_curve2      = gcurve(color=color.green, graph=curve7)
m_curve3      = gcurve(color=color.red,   graph=curve7)

dt = 1
t = 0

handled1 = False
handled2 = False
handled3 = False
changed1 = False  # make sure the program will not go to wrong state
changed2 = False
changed3 = False

while True:
	
	rate(300)  
	lucky_angle = (pi/2)-diff_angle(rocket3.r.pos,rocket3.v) 
	first_cosmic_velocity = sqrt(G*earth.m/mag(rocket3.r.pos))
	t+=dt

	if rocket1.fuel_mass > 0  :

		rocketL.r.up   = rotate(rocketL.r.up,angle=-25*dt*pi/18000)
		
		total_mass = rocket1.total_mass() + rocket2.total_mass() + rocket3.total_mass()	
		dm = rocket1.mass_flow_rate * dt
		thrust = rocket1.exit_speed*norm(rocketL.r.up)*dm/dt

		gforce1=gforce2=gforce3 = g_force(total_mass,rocket1.r.pos)
		g1=g2=g3 = mag(gforce1) / total_mass 
		drag1=drag2=drag3 = drag_force(mag(rocket1.v),density_air(mag(rocket1.r.pos)-earth.radius),0.2,pi*SVF_radius**2)*norm(rocketL.r.up)

		a1=a2=a3 = (thrust + gforce1 + drag1) / total_mass

		rocket.v      += a1*dt
		rocket.r.pos  += rocket.v*dt
		rocketL.r.pos += rocket.v*dt

		# For plotting only
		rocket1.v += a1*dt
		rocket2.v += a2*dt
		rocket3.v += a3*dt
		rocket1.r.pos += rocket1.v*dt
		rocket2.r.pos += rocket2.v*dt
		rocket3.r.pos += rocket3.v*dt

		rocket1.fuel_mass -= dm
		scene.center = rocketL.r.compound_to_world(vec(0,-0.5*whole_rocketL.size.y+enlarge*(138*convert+24.8+18*0.3048-0.7*J2_height),0)) # stage3's start
	
	elif rocket1.fuel_mass < 0 and rocket2.fuel_mass > 0:
		
		if handled1 == False:
			rocket1L.r.pos  = rocketL.r.compound_to_world(vec(0,-0.5*whole_rocketL.size.y+0.5*stage1L.size.y,0))
			rocket1L.r.up = rocketL.r.up
			rocket1L.r.visible  = True

			rocket23L.r.pos  = rocketL.r.compound_to_world(vec(0,-0.5*whole_rocket.size.y+enlarge*(138*convert)+0.5*stage2_topL.size.y,0))
			rocket23L.r.up= rocketL.r.up
			rocket23L.r.visible = True

			rocketL.r.visible   = False
			handled1 = True

			print('First Stage separated')

		rocket1L.r.up  = rocket1.v
		rocket23L.r.up = rocket2.v

		total_mass = rocket2.total_mass() + rocket3.total_mass()
		dm = rocket2.mass_flow_rate*dt
		thrust = rocket2.exit_speed*norm(rocket23L.r.up)*dm/dt

		gforce2=gforce3 = g_force(total_mass,rocket2.r.pos)
		g2=g3 = mag(gforce2) / total_mass
		drag2=drag3 = drag_force(mag(rocket2.v),density_air(mag(rocket2.r.pos)-earth.radius),0.2,pi*SVS_radius**2)*norm(rocket23L.r.up)
		
		a2=a3 = (thrust + gforce2 + drag2) / total_mass

		rocket2.v += a2*dt
		rocket3.v += a3*dt
		rocket2.r.pos += rocket2.v*dt
		rocket3.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket2.v*dt

		rocket2.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0)) # stage3's start 

		# Handle stage1 which has separated
		gforce1 = g_force(rocket1.total_mass(),rocket1.r.pos)
		g1 = mag(gforce1) / rocket1.total_mass()

		if mag(rocket1.r.pos) > earth.radius:
			a1 = gforce1 / rocket1.total_mass()
			rocket1.v += a1*dt
			rocket1.r.pos  += rocket1.v*dt
			rocket1L.r.pos += rocket1.v*dt
			rocket1L.r.up = rocket1.v
		else:
			a1 = vector(0,0,0)
			rocket1.v = vector(0,0,0)

	elif  rocket3.fuel_mass > 0 and changed1 == False:
		
		if handled2 == False:

			rocket2L.r.pos  = rocket23L.r.compound_to_world(vec(0,-0.5*stage2_topL.size.y+0.5*stage2L.size.y,0))
			rocket2L.r.up   = rocket23L.r.up
			rocket2L.r.visible = True

			rocket3L.r.pos  = rocket23L.r.compound_to_world(vec(0,-0.5*stage2_topL.size.y+0.5*topL.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
			rocket3L.r.up = rocket23L.r.up
			rocket3L.r.visible = True
			attach_trail(rocket3L.r)

			rocket23L.r.visible = False
			handled2 = True

			print('Second Stage separated')
		
		rocket3L.r.up = rocket3.v
		
		dm = rocket3.mass_flow_rate*dt
		thrust = rocket3.exit_speed*norm(rocket3L.r.up)*dm/dt

		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3 = mag(gforce3) / rocket3.total_mass()
		drag3 = drag_force(mag(rocket3.v),density_air(mag(rocket3.r.pos)-earth.radius),0.2,pi*SVT_radius**2)*norm(rocket3L.r.up)
				
		a3 = (thrust + gforce3 + drag3) / rocket3.total_mass()
		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged

		rocket3.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if mag(rocket3.v)*cos(lucky_angle) >= first_cosmic_velocity:			
			if handled3 == False:				
				handled3 = True
				changed1  = True
				print('turn off engine')
		
		# Handle stages which have separated				
		
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()
		gforce1 = g_force(rocket1.total_mass(),rocket1.r.pos)
		g1 = mag(gforce1) / rocket1.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = gforce2 / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:	
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)

		if mag(rocket1.r.pos) > earth.radius:
			a1 = gforce1 / rocket1.total_mass()
			rocket1.v += a1*dt
			rocket1.r.pos += rocket1.v*dt
			rocket1L.r.pos += rocket1.v*dt
			rocket1L.r.up = rocket1.v
		else:
			a1 = vector(0,0,0)
			rocket1.v = vector(0,0,0)
			
	elif changed2 == False:
	
		rocket3L.r.up = rocket3.v
		
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3      = mag(gforce3) / rocket3.total_mass()
		a3      = gforce3 / rocket3.total_mass()

		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt

		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if abs(lucky_angle)<=0.0002 and  mag(rocket3.v)*cos(lucky_angle) < first_cosmic_velocity:
			changed2 = True
			print('turn on engine')

		# Handle stage2 which have separated
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = gforce2 / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:	
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)
	
	elif changed3 == False:

		rocket3L.r.up = rocket3.v

		dm = rocket3.mass_flow_rate*dt
		thrust = rocket3.exit_speed*norm(rocket3L.r.up)*dm/dt

		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3 = mag(gforce3) / rocket3.total_mass()
		drag3 = drag_force(mag(rocket3.v),density_air(mag(rocket3.r.pos)-earth.radius),0.2,pi*SVT_radius**2)*norm(rocket3L.r.up)
				
		a3 = (thrust + gforce3 + drag3) / rocket3.total_mass()
		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged

		rocket3.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if abs(lucky_angle)<=0.0002 and  mag(rocket3.v)*cos(lucky_angle) >= first_cosmic_velocity:	
			print('turn off engine')
			changed3=True
		
		# Handle stage2 which have separated
		
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = gforce2 / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)

	else:
		
		rocket3L.r.up = rocket3.v

		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3      = mag(gforce3) / rocket3.total_mass()
		a3      = gforce3 / rocket3.total_mass()

		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt

		rocket23L.r.pos += rocket3.v*dt  # for keeping scene.center unchanged
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))

		# Handle stage2 which has separated

		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = gforce2 / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)

	height_curve1.plot(pos=(t,mag(rocket1.r.pos)-earth.radius))
	height_curve2.plot(pos=(t,mag(rocket2.r.pos)-earth.radius))
	height_curve3.plot(pos=(t,mag(rocket3.r.pos)-earth.radius))
	v_curve1.plot(pos=(t,mag(rocket1.v)))
	v_curve2.plot(pos=(t,mag(rocket2.v)))
	v_curve3.plot(pos=(t,mag(rocket3.v)))
	a_curve1.plot(pos=(t,mag(a1)))
	a_curve2.plot(pos=(t,mag(a2)))
	a_curve3.plot(pos=(t,mag(a3)))
	angle_curve1.plot(pos=(t,diff_angle(rocket1L.r.up,rocket1.r.pos)))
	angle_curve2.plot(pos=(t,diff_angle(rocket2L.r.up,rocket2.r.pos)))
	angle_curve3.plot(pos=(t,diff_angle(rocket3L.r.up,rocket3.r.pos)))
	g_curve1.plot(pos=(t,g1))
	g_curve2.plot(pos=(t,g2))
	g_curve3.plot(pos=(t,g3))
	d_curve1.plot(pos=(t,mag(drag1)))
	d_curve2.plot(pos=(t,mag(drag2)))
	d_curve3.plot(pos=(t,mag(drag3)))
	m_curve1.plot(pos=(t,rocket1.fuel_mass))
	m_curve2.plot(pos=(t,rocket2.fuel_mass))
	m_curve3.plot(pos=(t,rocket3.fuel_mass))
	
   

