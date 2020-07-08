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
curve6 = graph(title ='gmoon-t',xtitle='time',ytitle='gforce'                   ,width=300,height=300,align='none')
curve7 = graph(title ='d-t'    ,xtitle='time',ytitle='drag force'          		,width=300,height=300,align='none')
curve8 = graph(title ='m-t'    ,xtitle='time',ytitle='fuel_mass'                ,width=300,height=300,align='none')

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
gforcemoon1   = gcurve(color=color.blue,  graph=curve6)
gforcemoon2   = gcurve(color=color.green, graph=curve6)
gforcemoon3   = gcurve(color=color.red,   graph=curve6)
d_curve1      = gcurve(color=color.blue,  graph=curve7)
d_curve2      = gcurve(color=color.green, graph=curve7)
d_curve3      = gcurve(color=color.red,   graph=curve7)
m_curve1      = gcurve(color=color.blue,  graph=curve8)
m_curve2      = gcurve(color=color.green, graph=curve8)
m_curve3      = gcurve(color=color.red,   graph=curve8)

dt = 10
t = 0

handled1 = False
handled2 = False
handled3 = False
changed1 = False  # make sure the program will not go to wrong state
changed2 = False
changed3 = False
changed4 = False
count=0
first_cosmic_velocity = 0

while True:
	rate(150)
	
	lucky_angle      = (pi/2)-diff_angle(rocket3.r.pos         ,rocket3.v) 
	lucky_angle_moon = (pi/2)-diff_angle(rocket3.r.pos-moon.pos,rocket3.v)
	first_cosmic_velocity       = sqrt(1*G*earth.m/mag(rocket3.r.pos))
	second_cosmic_velocity      = sqrt(2*G*earth.m/mag(rocket3.r.pos))
	first_cosmic_velocity_moon  = sqrt(1*G*moon.m /mag(rocket3.r.pos))
	second_cosmic_velocity_moon = sqrt(2*G*moon.m /mag(rocket3.r.pos-moon.pos))
	t+=dt

	moon.a = g_force(moon.m,moon.pos)/moon.m
	moon.v   += moon.a*dt
	moon.pos += moon.v*dt

	if rocket1.fuel_mass > 0  :
			
		rocketL.r.up   = rotate(rocketL.r.up,angle=-250*pi/18000)

		total_mass = rocket1.total_mass() + rocket2.total_mass() + rocket3.total_mass()	
		dm = rocket1.mass_flow_rate * dt
		thrust = rocket1.exit_speed*norm(rocketL.r.up)*dm/dt

		gfmr1=gfmr2=gfmr3 = gfmoon(total_mass,rocket1.r.pos-moon.pos) 
		gfma1=gfma2=gfma3 = mag(gfmr1) / total_mass
		gforce1=gforce2=gforce3 = g_force(total_mass,rocket1.r.pos)
		g1=g2=g3 = mag(gforce1) / total_mass 
		drag1=drag2=drag3 = drag_force(mag(rocket1.v),density_air(mag(rocket1.r.pos)-earth.radius),0.2,pi*SVF_radius**2)*norm(rocketL.r.up)
		a1=a2=a3 = (thrust + gforce1 + drag1 + gfmr1) / total_mass

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

		gfmr2=gfmr3 = gfmoon(total_mass,rocket2.r.pos-moon.pos)
		gfma2=gfma3 = mag(gfmr2)/total_mass
		gforce2=gforce3 = g_force(total_mass,rocket2.r.pos)
		g2=g3 = mag(gforce2) / total_mass
		drag2=drag3 = drag_force(mag(rocket2.v),density_air(mag(rocket2.r.pos)-earth.radius),0.2,pi*SVS_radius**2)*norm(rocket23L.r.up)
		
		a2=a3 = (thrust + gforce2 + drag2 + gfmr2) / total_mass
		
		rocket2.v += a2*dt
		rocket3.v += a3*dt
		rocket2.r.pos += rocket2.v*dt
		rocket3.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket2.v*dt

		rocket2.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0)) # stage3's start 

		# Handle stage1 which has separated
		gfmr1 = gfmoon(total_mass,rocket1.r.pos-moon.pos)
		gforce1 = g_force(rocket1.total_mass(),rocket1.r.pos)
		g1 = mag(gforce1) / rocket1.total_mass()
		gfma1=mag(gfmr1)/rocket1.total_mass()

		if mag(rocket1.r.pos) > earth.radius:
			a1 = (gforce1 + gfmr1) / rocket1.total_mass()
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
		
		gfmr3 = gfmoon(rocket3.total_mass(),rocket3.r.pos-moon.pos)
		gfma3 = mag(gfmr3)/rocket3.total_mass()
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3 = mag(gforce3) / rocket3.total_mass()
		drag3 = drag_force(mag(rocket3.v),density_air(mag(rocket3.r.pos)-earth.radius),0.2,pi*SVT_radius**2)*norm(rocket3L.r.up)
				
		a3 = (thrust + gforce3 + drag3 + gfmr3 ) / rocket3.total_mass()
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

		gfmr2 = gfmoon(rocket2.total_mass(),rocket2.r.pos-moon.pos)
		gfmr1 = gfmoon(rocket1.total_mass(),rocket1.r.pos-moon.pos)
		gfma2 = mag(gfmr2)/rocket2.total_mass()
		gfma1 = mag(gfmr1)/rocket1.total_mass()
		
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		gforce1 = g_force(rocket1.total_mass(),rocket1.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()
		g1 = mag(gforce1) / rocket1.total_mass()

		if mag(rocket2.r.pos) > earth.radius:	
			a2 = (gforce2 + gfmr2) / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:	
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)

		if mag(rocket1.r.pos) > earth.radius:
			a1 = (gforce1 + gfmr1) / rocket1.total_mass()
			rocket1.v += a1*dt
			rocket1.r.pos += rocket1.v*dt
			rocket1L.r.pos += rocket1.v*dt
			rocket1L.r.up = rocket1.v
		else:
			a1 = vector(0,0,0)
			rocket1.v = vector(0,0,0)
			
	elif changed2 == False: # Not using fuel
		
		rocket3L.r.up = rocket3.v

		gfmr3 = gfmoon(rocket3.total_mass(),rocket3.r.pos-moon.pos)
		gfma3 = mag(gfmr3)/rocket3.total_mass()
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3      = mag(gforce3) / rocket3.total_mass()
		a3      = (gforce3 + gfmr3)/ rocket3.total_mass()

		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt

		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if rocket3.fuel_mass < 0:
			changed2 = True
			changed3 = True
		
		elif  abs(lucky_angle)<=0.0002 and  mag(rocket3.v)*cos(lucky_angle) <= first_cosmic_velocity :
			changed2 = True
			print('turn on engine')
		
		# Handle stage 2 which have separated		
		
		gfmr2 = gfmoon(rocket2.total_mass(),rocket2.r.pos-moon.pos)
		gfma2 = mag(gfmr2)/rocket2.total_mass()
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = (gforce2 + gfmr2) / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos  += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)
	
	elif changed3 == False: # Turn on fuel

		rocket3L.r.up = rocket3.v
	
		dm = rocket3.mass_flow_rate*dt
		thrust = rocket3.exit_speed*norm(rocket3L.r.up)*dm/dt

		gfmr3 = gfmoon(rocket3.total_mass(),rocket3.r.pos-moon.pos)
		gfma3 = mag(gfmr3)/rocket3.total_mass()
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3 = mag(gforce3) / rocket3.total_mass()
		drag3 = drag_force(mag(rocket3.v),density_air(mag(rocket3.r.pos)-earth.radius),0.2,pi*SVT_radius**2)*norm(rocket3L.r.up)
				
		a3 = (thrust + gforce3 + drag3 + gfmr3) / rocket3.total_mass()
		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged

		rocket3.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if rocket3.fuel_mass < 0 :	
			changed2=True
			changed3=True

		elif count==0 and abs(lucky_angle)<=0.0002 and  mag(rocket3.v)*cos(lucky_angle) >= first_cosmic_velocity:
			print('turn off engine')
			changed3=True
			count+=1
		
		elif abs(mag(rocket3.v)*cos(lucky_angle)) >= second_cosmic_velocity:
			changed3=True
			count+=1
		
		# Handle stage 2 which have separated		
		
		gfmr2 = gfmoon(rocket2.total_mass(),rocket2.r.pos-moon.pos)
		gfma2 = mag(gfmr2)/rocket2.total_mass()
		gforce2 = g_force(rocket2.total_mass(),rocket2.r.pos)
		g2 = mag(gforce2) / rocket2.total_mass()

		if mag(rocket2.r.pos) > earth.radius:
			a2 = (gforce2 + gfmr2) / rocket2.total_mass()
			rocket2.v += a2*dt
			rocket2.r.pos  += rocket2.v*dt
			rocket2L.r.pos += rocket2.v*dt
			rocket2L.r.up = rocket2.v
		else:
			a2 = vector(0,0,0)
			rocket2.v = vector(0,0,0)

	elif changed4 == False: # Not using fuel
	
		rocket3L.r.up = rocket3.v

		gfmr3 = gfmoon(rocket3.total_mass(),rocket3.r.pos-moon.pos)
		gfma3 = mag(gfmr3)/rocket3.total_mass()
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3      = mag(gforce3) / rocket3.total_mass()
		a3      = (gforce3 + gfmr3 )/ rocket3.total_mass()

		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt

		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))

		if count==1 and t>=4430:
			changed3 = False
		elif count==2 and mag(rocket3.r.pos-moon.pos)<=4300000 :
			changed4 = True
			count+=1
			print('turn on engine to deaccelerate')

	elif changed4 == True: # Deaccelerate into moon orbit
		
		rocket3L.r.up = rocket3.v
	
		dm = rocket3.mass_flow_rate*dt
		thrust = -1*rocket3.exit_speed*norm(rocket3L.r.up)*dm/dt

		gfmr3 = gfmoon(rocket3.total_mass(),rocket3.r.pos-moon.pos)
		gfma3 = mag(gfmr3)/rocket3.total_mass()
		gforce3 = g_force(rocket3.total_mass(),rocket3.r.pos)
		g3 = mag(gforce3) / rocket3.total_mass()
		drag3 = drag_force(mag(rocket3.v),density_air(mag(rocket3.r.pos)-earth.radius),0.2,pi*SVT_radius**2)*norm(rocket3L.r.up)
				
		a3 = (thrust + gforce3 + drag3 + gfmr3) / rocket3.total_mass()
		rocket3.v      += a3*dt
		rocket3.r.pos  += rocket3.v*dt
		rocket3L.r.pos += rocket3.v*dt
		rocket23L.r.pos += rocket3.v*dt # for keeping scene.center unchanged

		rocket3.fuel_mass -= dm
		scene.center = rocket23L.r.compound_to_world(vec(0,-0.5*rocket23L.r.size.y+enlarge*(24.8+18*0.3048-0.7*J2_height),0))
		
		if rocket3.fuel_mass<=0 or mag(rocket3.v)<=first_cosmic_velocity_moon:
			changed4 = False
			print('turn off engine and start rotating around the moon')
		
	height_curve1.plot(pos=(t,(mag(rocket1.r.pos)-earth.radius)/1000))
	height_curve2.plot(pos=(t,(mag(rocket2.r.pos)-earth.radius)/1000))
	height_curve3.plot(pos=(t,(mag(rocket3.r.pos)-earth.radius)/1000))
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
	gforcemoon1.plot(pos=(t,gfma1))
	gforcemoon2.plot(pos=(t,gfma2))
	gforcemoon3.plot(pos=(t,gfma3))
	d_curve1.plot(pos=(t,mag(drag1)))
	d_curve2.plot(pos=(t,mag(drag2)))
	d_curve3.plot(pos=(t,mag(drag3)))
	m_curve1.plot(pos=(t,rocket1.fuel_mass))
	m_curve2.plot(pos=(t,rocket2.fuel_mass))
	m_curve3.plot(pos=(t,rocket3.fuel_mass))
	
   

