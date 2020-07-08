from vpython import *

# Constants for building different stages of rockets
convert=0.3048
F1_radius=6.1*convert
F1_height=18.5*convert
SVF_radius=33*convert*(1/2)
SVF_height=(138-18.5*0.7)*convert
SVS_radius=SVF_radius
SVS_height=(24.8-3.4*0.7)
J2_radius=3.4*convert
J2_height=3.4
SVT_radius=21.7*0.5*convert
SVT_height=61.6*convert-18*0.3048
Top1_height=32.4*convert
Top1_radius=0.6*SVT_radius
apollo_radius=Top1_radius
apollo_height=0.5*2*Top1_height/3
apollotop_height=0.5*1*Top1_height/3
apollotop_radius=apollo_radius
verytop_radius=(1/6)*apollo_radius
verytop_height=2*apollo_height+1
verytop2_radius=(1/3)*apollo_radius
verytop2_height=(4/5)*apollo_height+1
verytop3_height=1
lastcone_height=1
color_rocket=vec(128/255,128/255,128/255)

# Building Earth and moon
mass       = {'earth': 5.97237E24,'moon':7.477E22} # in kg
radius     = {'earth': 6.371E6,'moon': 1.7371E6}   # in m
moon_orbit = {'r': 3.84E8, 'v': 1.022E3}

earth    = sphere(pos = vector(0,0,0), radius = radius['earth'], texture = {'file':textures.earth}) 
earth.m  = mass['earth']
earth.up = vec(1*sin(80.39*pi/180)*cos(28.35*pi/180),sin(28.35*pi/180),-1*cos(28.35*pi/180)*cos(80.39*pi/180))
earth.rotate(angle=61.65*pi/180, axis=vec(0,1,0))

moon   = sphere(pos=vector(moon_orbit['r'],0,0),radius=radius['moon'],texture={'file':textures.rough})
moon.m = mass['moon']
moon.v = vec(0,moon_orbit['v'],0)

# Stage1----------------------------------------------------------------------------------------------
F11=cone(pos=vec(0,0,0),axis=vec(0,F1_height,0),radius=F1_radius,color=color_rocket)
F12=cone(pos=vec(SVF_radius,0,0),axis=vec(0,F1_height,0),radius=F1_radius,color=color_rocket)
F13=cone(pos=vec(0,0,SVF_radius),axis=vec(0,F1_height,0),radius=F1_radius,color=color_rocket)
F14=cone(pos=vec(-1*SVF_radius,0,0),axis=vec(0,F1_height,0),radius=F1_radius,color=color_rocket)
F15=cone(pos=vec(0,0,-1*SVF_radius),axis=vec(0,F1_height,0),radius=F1_radius,color=color_rocket)

SVF=cylinder(pos=vec(0,F1_height*0.7,0),axis=vec(0,SVF_height,0),radius=SVF_radius)

deco1=cone(pos=vec(SVF_radius,F1_height*0.6,0),axis=vec(0,1.5*F1_height,0),radius=1.1*F1_radius)
deco2=cone(pos=vec(0,F1_height*0.6,SVF_radius),axis=vec(0,1.5*F1_height,0),radius=1.1*F1_radius)
deco3=cone(pos=vec(-1*SVF_radius,F1_height*0.6,0),axis=vec(0,1.5*F1_height,0),radius=1.1*F1_radius)
deco4=cone(pos=vec(0,F1_height*0.6,-1*SVF_radius),axis=vec(0,1.5*F1_height,0),radius=1.1*F1_radius)

a=3*F1_radius
b=(1/2)*F1_radius
c=SVF_radius+F1_radius-(1/2)*a
taila=(1/2)*a-(b/(2*sqrt(5)))+c
tailb=a/(2*sqrt(5))+1.5+F1_height*0.5

tail1=box(pos=vec(SVF_radius+F1_radius,1.5+F1_height*0.5,0),length=3*F1_radius,height=(1/2)*F1_radius,width=0.2,color=color_rocket)
tail2=box(pos=vec(taila,tailb,0),length=(sqrt(6)/sqrt(5))*a,height=(1/2)*F1_radius*(sqrt(6)/sqrt(5)),width=0.2,axis=vec(-sqrt(5),1,0),color=color_rocket)
tail3=box(pos=vec(SVF_radius+F1_radius,2+F1_height*0.5,0),length=F1_radius,height=(1/2)*F1_radius,width=0.2,color=color_rocket)

tail4=box(pos=vec(-1*(SVF_radius+F1_radius),1.5+F1_height*0.5,0),length=3*F1_radius,height=(1/2)*F1_radius,width=0.2,color=color_rocket)
tail5=box(pos=vec(-1*taila,tailb,0),length=(sqrt(6)/sqrt(5))*a,height=(1/2)*F1_radius*(sqrt(6)/sqrt(5)),width=0.2,axis=vec(sqrt(5),1,0),color=color_rocket)
tail6=box(pos=vec(-1*(SVF_radius+F1_radius),2+F1_height*0.5,0),length=F1_radius,height=(1/2)*F1_radius,width=0.2,color=color_rocket)

tail7=box(pos=vec(0,1.5+F1_height*0.5,SVF_radius+F1_radius),length=3*F1_radius,height=(1/2)*F1_radius,width=0.2,axis=vec(0,0,1),color=color_rocket)
tail8=box(pos=vec(0,tailb,taila),length=(sqrt(6)/sqrt(5))*a,height=(1/2)*F1_radius*(sqrt(6)/sqrt(5)),width=0.2,axis=vec(0,1,-1*sqrt(5)),up=vec(0,sqrt(5),1),color=color_rocket)
tail9=box(pos=vec(0,2+F1_height*0.5,SVF_radius+F1_radius),length=F1_radius,height=(1/2)*F1_radius,width=0.2,axis=vec(0,0,1),color=color_rocket)

tail10=box(pos=vec(0,1.5+F1_height*0.5,-1*(SVF_radius+F1_radius)),length=3*F1_radius,height=(1/2)*F1_radius,width=0.2,axis=vec(0,0,-1),color=color_rocket)
tail11=box(pos=vec(0,tailb,-1*taila),length=(sqrt(6)/sqrt(5))*a,height=(1/2)*F1_radius*(sqrt(6)/sqrt(5)),width=0.2,axis=vec(0,1,1*sqrt(5)),up=vec(0,sqrt(5),-1),color=color_rocket)
tail12=box(pos=vec(0,2+F1_height*0.5,-1*(SVF_radius+F1_radius)),length=F1_radius,height=(1/2)*F1_radius,width=0.2,axis=vec(0,0,-1),color=color_rocket)

#second stage----------------------------------------------------------------------------------------------

J21=cone(pos=vec(0,138*convert,0),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)
J22=cone(pos=vec(SVF_radius-J2_radius-1,138*convert,0),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)
J23=cone(pos=vec(0,138*convert,(SVF_radius-J2_radius-1)),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)
J24=cone(pos=vec(-1*(SVF_radius-J2_radius-1),138*convert,0),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)
J25=cone(pos=vec(0,138*convert,-1*(SVF_radius-J2_radius-1)),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)

SVS=cylinder(pos=vec(0,138*convert+J2_height*0.7,0),axis=vec(0,SVS_height,0),radius=SVF_radius)
contact2=extrusion(path=paths.circle(radius=SVF_radius) , shape=shapes.rectangle(pos=[0,0.5*J2_height+138*convert],width=0.2,height=J2_height),color=color_rocket)

#thrid stage----------------------------------------------------------------------------------------------

J26=cone(pos=vec(0,138*convert+24.8+18*0.3048-0.7*J2_height,0),axis=vec(0,J2_height,0),radius=J2_radius,color=color_rocket)
contact3=extrusion(path=paths.circle(radius=SVS_radius) , shape=shapes.line(start=(SVS_radius,138*convert+24.8), end=(SVT_radius,138*convert+24.8+18*0.3048),pos=[-SVS_radius,0]),color=color_rocket)
SVT=cylinder(pos=vec(0,138*convert+24.8+18*0.3048,0),axis=vec(0,SVT_height,0),radius=SVT_radius)

#top1----------------------------------------------------------------------------------------------
topy=138*convert+24.8+18*0.3048+SVT_height
contact4=extrusion(path=paths.circle(radius=SVT_radius), shape=shapes.line(start=(SVT_radius,topy), end=(Top1_radius,topy+Top1_height),pos=[-SVT_radius,0]))
#apollo----------------------------------------------------------------------------------------------
apollo=cylinder(pos=vec(0,topy+Top1_height,0),axis=vec(0,apollo_height,0),radius=apollo_radius,color=color_rocket)
apollotop=cone(pos=vec(0,topy+Top1_height+apollo_height,0),axis=vec(0,apollotop_height,0),radius=apollotop_radius,color=color_rocket)
#verytop----------------------------------------------------------------------------------------------
verytop1=cylinder(pos=vec(0,topy+Top1_height+apollo_height+apollotop_height-1,0),axis=vec(0,verytop_height,0),radius=verytop_radius)
verytop3=cone(pos=vec(0,topy+Top1_height+apollo_height+apollotop_height-1+verytop_height,0),axis=vec(0,verytop3_height,0),radius=verytop_radius)
verytop2=cylinder(pos=vec(0,topy+Top1_height+apollo_height+apollotop_height-1,0),axis=vec(0,verytop2_height,0),radius=verytop2_radius)
lastcone=cone(pos=vec(0,topy+Top1_height+apollo_height+apollotop_height-1+verytop2_height,0),axis=vec(0,lastcone_height,0),radius=verytop2_radius)

stage1    = compound([F11,F12,F13,F14,F15,SVF,deco1,deco2,deco3,deco4,tail1,tail2,tail3,tail4,tail5,tail6,tail7,tail8,tail9,tail10,tail11,tail12])
stage2    = compound([J21,J22,J23,J24,J25,SVS,contact2])
stage3    = compound([J26,contact3,SVT])
topapollo = compound([contact4,apollo,apollotop])
verytop   = compound([verytop1,verytop2,verytop3,lastcone])
top       = compound([stage3,topapollo,verytop])

stage1_1 = stage1.clone()
stage2_1 = stage2.clone()
stage2_2 = stage2.clone()
top_1    = top.clone()
top_2    = top.clone()

whole_rocket = compound([stage1_1,stage2_1,top_1])
stage2_top   = compound([stage2_2,top_2])

stage1L       = stage1.clone()
stage2L       = stage2.clone()
topL          = top.clone()
stage2_topL   = stage2_top.clone()
whole_rocketL = whole_rocket.clone()

stage1.pos       += vec(0,earth.radius,0)
stage2.pos       += vec(0,earth.radius,0)
top.pos          += vec(0,earth.radius,0)
stage2_top.pos   += vec(0,earth.radius,0)
whole_rocket.pos += vec(0,earth.radius,0)

stage1.visible       = False
stage2.visible       = False
top.visible          = False
stage2_top.visible   = False
whole_rocket.visible = False

# Create stages of rockets that are enlarged (and can be seen at some moment)
enlarge = 300

stage1L.size       *= enlarge
stage2L.size       *= enlarge
topL.size          *= enlarge
stage2_topL.size   *= enlarge
whole_rocketL.size *= enlarge

stage2_topL.pos   += vec(0,earth.radius + 0.5*stage2_topL.size.y  ,0) 
whole_rocketL.pos += vec(0,earth.radius + 0.5*whole_rocketL.size.y,0)
stage1L.pos       += vec(0,earth.radius + 0.5*stage1L.size.y      ,0)
stage2L.pos       += vec(0,earth.radius + enlarge*stage2L.pos.y   ,0)
topL.pos          += vec(0,earth.radius + enlarge*topL.pos.y      ,0)

stage2_topL.visible   = False
stage1L.visible       = False    
stage2L.visible       = False
topL.visible          = False
whole_rocketL.visible = True

scene.center = whole_rocketL.compound_to_world(vec(0,-0.5*whole_rocketL.size.y+enlarge*138*convert,0))

'''if __name__ == '__main__':
    dt = 0.01
    v = vector(0,10000,0)

    while True:
        rate(1000)
        whole_rocketL.pos += v*dt        
'''