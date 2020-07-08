from vpython import *
from saturnV import *

G = 6.67408E-11 # gravitional constant

class Rocket():
    def __init__(self,mass=1,fuel_mass=1,thrust=1,burn_time=1,stage=0):
        
        # Attributes for stage1,stage2,top
        self.mass = mass
        self.fuel_mass = fuel_mass
        self.mass_flow_rate = fuel_mass / burn_time
        self.exit_speed = thrust / self.mass_flow_rate

        # Connect with different stages of rockets
        if stage == 1:
            self.r = stage1
        elif stage == '1L':
            self.r = stage1L
        elif stage == 2:
            self.r = stage2
        elif stage == '2L':
            self.r = stage2L
        elif stage == 3:
            self.r = top
        elif stage == '3L':
            self.r = topL
        elif stage == '2+3':   
            self.r = stage2_top
        elif stage == '2+3L':
            self.r = stage2_topL
        elif stage == 'all':
            self.r = whole_rocket
        elif stage == 'allL':
            self.r = whole_rocketL
        else:
            print('Error')

        self.v=vec(465*cos(28.35*pi/180),0,0) # velocity due to earth's rotational speed

    def total_mass(self): 
        return self.mass + self.fuel_mass

    def __str__(self):
        return ('I am a rocket :)')

def g_force(mass_of_rocket,pos):
    '''gravitional force of earth to rocket'''
    return -G*earth.m*mass_of_rocket / mag2(pos) * norm(pos)
def gfmoon(mass_of_rocket,pos):
    return -G*moon.m*mass_of_rocket  / mag2(pos) * norm(pos)

def density_air(height):
    ''' density (in kg/m^3) at specific height, assume temperature follows standard lapse rate'''
    
    g = 9.80665   # gravitional acceleration near ground
    M = 0.0289644 # Molar mass of earth's air (in kg/mol)
    R = 8.3144598 # Universal gas constant for air (in Nm/molK)

    d_init = [1.225,0.36391,0.08803,0.01322,0.00143,0.00086,0.000064] # Mass density at different subscript b (in kg/m^3)
    T_init = [288.15,216.65,216.65,228.65,270.65,270.65,214.65]       # Standard Temperature at different subscript b (in K)
    L      = [-0.0065,0,0.001,0.0028,0,-0.0028,-0.002]                # Temperature Lapse Rate (in K/m)
    
    if height < 11000:
        d=d_init[0]*(T_init[0]/(T_init[0]+L[0]*(height-0)))**(1+(g*M/(R*L[0])))
    elif height< 20000:
        d=d_init[1]*exp((-1*g*M*(height-11000))/(R*T_init[1]))
    elif height< 32000:
        d=d_init[2]*(T_init[2]/(T_init[2]+L[2]*(height-20000)))**(1+(g*M/(R*L[2])))
    elif height< 47000:
        d=d_init[3]*(T_init[3]/(T_init[3]+L[3]*(height-32000)))**(1+(g*M/(R*L[3])))
    elif height< 51000:
        d=d=d_init[4]*exp((-1*g*M*(height-47000))/(R*T_init[4]))
    elif height< 71000:
        d=d_init[5]*(T_init[5]/(T_init[5]+L[5]*(height-51000)))**(1+(g*M/(R*L[5])))
    elif height<= 86000:
        d=d_init[6]*(T_init[6]/(T_init[6]+L[6]*(height-86000)))**(1+(g*M/(R*L[6])))
    else: 
        d=0
    
    return d 

def drag_force(v, density_air, Cd,A):
    ''' Fd = 0.5*density_air* v^2 * Constant * reference Area'''
    return -0.5 * density_air * (v**2)* Cd * A

if __name__ == '__main__':
    print('Success')

    
