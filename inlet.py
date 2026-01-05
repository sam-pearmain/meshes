import gmsh
from math import radians, tan

DOMAIN_LENGTH, DOMAIN_HEIGHT = 500, 250
INTAKE_LENGTH, INTAKE_HEIGHT = 150, 44
THROAT_HEIGHT, RAMP_LENGTH = 15, 81.7
RAMP_ANGLE_ONE, RAMP_ANGLE_TWO = 10, 22
COWL_ANGLE, COWL_HEIGHT = 30, 8
KINK_LENGTH = (
    (tan(radians(RAMP_ANGLE_ONE)) - INTAKE_HEIGHT - COWL_HEIGHT) / 
    (tan(radians(RAMP_ANGLE_TWO)) - tan(radians(RAMP_ANGLE_ONE)))
)
KINK_HEIGHT = tan(RAMP_ANGLE_ONE) * KINK_LENGTH

def main():
    gmsh.initialize()
    gmsh.model.add("inlet")
    
    # domain bounds
    p1 = gmsh.model.geo.addPoint(0, 0, 0)
    p2 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, 0, 0)
    p3 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, DOMAIN_HEIGHT, 0)
    p4 = gmsh.model.geo.addPoint(0, DOMAIN_HEIGHT, 0)
    
    # inlet points
    p5 = gmsh.model.geo.addPoint(DOMAIN_LENGTH - INTAKE_LENGTH, 0, 0)
    p6 = gmsh.model.geo.addPoint(DOMAIN_LENGTH - INTAKE_LENGTH + KINK_LENGTH, KINK_HEIGHT, 0)
    p7 = gmsh.model.geo.addPoint(RAMP_LENGTH, INTAKE_HEIGHT - COWL_HEIGHT - THROAT_HEIGHT, 0)
    p8 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, INTAKE_HEIGHT - COWL_HEIGHT - THROAT_HEIGHT, 0)

    # cowl points
    p9 = gmsh.model.geo.addPoint(DOMAIN_LENGTH - INTAKE_LENGTH + RAMP_LENGTH, INTAKE_HEIGHT - COWL_HEIGHT, 0)
    p10 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, INTAKE_HEIGHT - COWL_HEIGHT, 0)
    p11 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, INTAKE_HEIGHT, 0)
    p12 = gmsh.model.geo.addPoint(DOMAIN_LENGTH - INTAKE_LENGTH + RAMP_LENGTH + (8 / tan(COWL_ANGLE)), INTAKE_HEIGHT, 0)

    # lines
    

if __name__ == "__main__":
    main()
