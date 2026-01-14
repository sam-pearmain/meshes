import gmsh
from math import radians, tan

# --- Constants ---
L0 = 150.0

# Geometry
DOMAIN_LENGTH, DOMAIN_HEIGHT = 1.04 * L0, 0.4 * L0
INTAKE_LENGTH, INTAKE_HEIGHT = 150.0, 44.0
THROAT_HEIGHT, RAMP_LENGTH = 15.0, 81.7
RAMP_HEIGHT = 21.0
RAMP_ANGLE_ONE, RAMP_ANGLE_TWO = 10.0, 22.0
COWL_ANGLE, COWL_HEIGHT = 30.0, 8.0

# Derived Geometrics
KINK_LENGTH = (RAMP_HEIGHT - tan(radians(RAMP_ANGLE_TWO)) * RAMP_LENGTH) / (
    tan(radians(RAMP_ANGLE_ONE)) - tan(radians(RAMP_ANGLE_TWO))
)
KINK_HEIGHT = tan(radians(RAMP_ANGLE_ONE)) * KINK_LENGTH
Y_SPLIT = RAMP_HEIGHT + THROAT_HEIGHT  # The logical split line (y approx 36.0)

# X-Coordinates
x_start = 0.0
x_ramp_start = DOMAIN_LENGTH - INTAKE_LENGTH
x_kink = x_ramp_start + KINK_LENGTH
x_throat_start = x_ramp_start + RAMP_LENGTH
x_cowl_tip = x_throat_start + (COWL_HEIGHT / tan(radians(COWL_ANGLE)))
x_end = DOMAIN_LENGTH

# --- Grid Resolution ---
total_divisions = 1024
total_length = DOMAIN_LENGTH

# Streamwise Counts
NX_1 = int(round(((x_ramp_start - x_start) / total_length) * total_divisions))
NX_2 = int(round(((x_kink - x_ramp_start) / total_length) * total_divisions))
NX_3 = int(round(((x_throat_start - x_kink) / total_length) * total_divisions))
NX_COWL = int(round(((x_cowl_tip - x_throat_start) / total_length) * total_divisions))
NX_WAKE = int(round(((x_end - x_cowl_tip) / total_length) * total_divisions))
NX_THROAT = NX_COWL + NX_WAKE

# --- VERTICAL CLUSTERING UPDATE ---
# Total = 500
# Shifted heavily to the "Wall/Throat" layer (Bottom)
NY_WALL = 400 
NY_FAR = 100

def main():
    gmsh.initialize()
    gmsh.model.add("inlet-structured-highres")
    lc = 1.0 

    # --- Points ---
    # 1. Bottom Line
    p1 = gmsh.model.geo.addPoint(x_start, 0, 0, lc)
    p5 = gmsh.model.geo.addPoint(x_ramp_start, 0, 0, lc)
    p6 = gmsh.model.geo.addPoint(x_kink, KINK_HEIGHT, 0, lc)
    p7 = gmsh.model.geo.addPoint(x_throat_start, RAMP_HEIGHT, 0, lc)
    p8 = gmsh.model.geo.addPoint(x_end, RAMP_HEIGHT, 0, lc)

    # 2. Split Line (Cowl Level)
    p17 = gmsh.model.geo.addPoint(x_start, Y_SPLIT, 0, lc)         
    p18 = gmsh.model.geo.addPoint(x_ramp_start, Y_SPLIT, 0, lc)    
    p19 = gmsh.model.geo.addPoint(x_kink, Y_SPLIT, 0, lc)          
    p9  = gmsh.model.geo.addPoint(x_throat_start, Y_SPLIT, 0, lc)
    
    # Cowl Top/Wake
    p12 = gmsh.model.geo.addPoint(x_cowl_tip, INTAKE_HEIGHT, 0, lc)
    p11 = gmsh.model.geo.addPoint(x_end, INTAKE_HEIGHT, 0, lc)
    p10 = gmsh.model.geo.addPoint(x_end, Y_SPLIT, 0, lc)

    # 3. Top Line
    p4  = gmsh.model.geo.addPoint(x_start, DOMAIN_HEIGHT, 0, lc)
    p13 = gmsh.model.geo.addPoint(x_ramp_start, DOMAIN_HEIGHT, 0, lc)
    p14 = gmsh.model.geo.addPoint(x_kink, DOMAIN_HEIGHT, 0, lc)
    p15 = gmsh.model.geo.addPoint(x_throat_start, DOMAIN_HEIGHT, 0, lc)
    p16 = gmsh.model.geo.addPoint(x_cowl_tip, DOMAIN_HEIGHT, 0, lc)
    p3  = gmsh.model.geo.addPoint(x_end, DOMAIN_HEIGHT, 0, lc)

    # --- Lines ---
    # Horizontal
    l_wall_1 = gmsh.model.geo.addLine(p1, p5)
    l_wall_2 = gmsh.model.geo.addLine(p5, p6)
    l_wall_3 = gmsh.model.geo.addLine(p6, p7)
    l_throat_bot = gmsh.model.geo.addLine(p7, p8)
    
    l_mid_1 = gmsh.model.geo.addLine(p17, p18)
    l_mid_2 = gmsh.model.geo.addLine(p18, p19)
    l_mid_3 = gmsh.model.geo.addLine(p19, p9)
    
    l_throat_top = gmsh.model.geo.addLine(p10, p9)
    l_cowl_top = gmsh.model.geo.addLine(p9, p12)
    l_cowl_back = gmsh.model.geo.addLine(p12, p11)

    l_top_1 = gmsh.model.geo.addLine(p4, p13)
    l_top_2 = gmsh.model.geo.addLine(p13, p14)
    l_top_3 = gmsh.model.geo.addLine(p14, p15)
    l_top_4 = gmsh.model.geo.addLine(p15, p16)
    l_top_5 = gmsh.model.geo.addLine(p16, p3)

    # Vertical
    l_inlet_bot = gmsh.model.geo.addLine(p1, p17)
    l_inlet_top = gmsh.model.geo.addLine(p17, p4)
    
    l_v1_bot = gmsh.model.geo.addLine(p5, p18)
    l_v1_top = gmsh.model.geo.addLine(p18, p13)
    
    l_v2_bot = gmsh.model.geo.addLine(p6, p19)
    l_v2_top = gmsh.model.geo.addLine(p19, p14)
    
    l_throat_inlet = gmsh.model.geo.addLine(p7, p9)
    l_v3 = gmsh.model.geo.addLine(p9, p15)
    
    l_v4 = gmsh.model.geo.addLine(p12, p16)
    l_out_int = gmsh.model.geo.addLine(p8, p10)
    l_out_ext = gmsh.model.geo.addLine(p11, p3)

    # --- Curve Loops ---
    cl1_b = gmsh.model.geo.addCurveLoop([l_wall_1, l_v1_bot, -l_mid_1, -l_inlet_bot])
    s1_b = gmsh.model.geo.addPlaneSurface([cl1_b])
    cl1_t = gmsh.model.geo.addCurveLoop([l_mid_1, l_v1_top, -l_top_1, -l_inlet_top])
    s1_t = gmsh.model.geo.addPlaneSurface([cl1_t])

    cl2_b = gmsh.model.geo.addCurveLoop([l_wall_2, l_v2_bot, -l_mid_2, -l_v1_bot])
    s2_b = gmsh.model.geo.addPlaneSurface([cl2_b])
    cl2_t = gmsh.model.geo.addCurveLoop([l_mid_2, l_v2_top, -l_top_2, -l_v1_top])
    s2_t = gmsh.model.geo.addPlaneSurface([cl2_t])

    cl3_b = gmsh.model.geo.addCurveLoop([l_wall_3, l_throat_inlet, -l_mid_3, -l_v2_bot])
    s3_b = gmsh.model.geo.addPlaneSurface([cl3_b])
    cl3_t = gmsh.model.geo.addCurveLoop([l_mid_3, l_v3, -l_top_3, -l_v2_top])
    s3_t = gmsh.model.geo.addPlaneSurface([cl3_t])

    cl4 = gmsh.model.geo.addCurveLoop([l_throat_bot, l_out_int, l_throat_top, -l_throat_inlet])
    s4 = gmsh.model.geo.addPlaneSurface([cl4])

    cl5 = gmsh.model.geo.addCurveLoop([l_cowl_top, l_v4, -l_top_4, -l_v3])
    s5 = gmsh.model.geo.addPlaneSurface([cl5])

    cl6 = gmsh.model.geo.addCurveLoop([l_cowl_back, l_out_ext, -l_top_5, -l_v4])
    s6 = gmsh.model.geo.addPlaneSurface([cl6])

    gmsh.model.geo.synchronize()

    # --- Transfinite Settings (X) ---
    for l in [l_wall_1, l_mid_1, l_top_1]: gmsh.model.mesh.setTransfiniteCurve(l, NX_1)
    for l in [l_wall_2, l_mid_2, l_top_2]: gmsh.model.mesh.setTransfiniteCurve(l, NX_2)
    for l in [l_wall_3, l_mid_3, l_top_3]: gmsh.model.mesh.setTransfiniteCurve(l, NX_3)
    
    for l in [l_throat_bot, l_throat_top]: gmsh.model.mesh.setTransfiniteCurve(l, NX_THROAT)
    for l in [l_cowl_top, l_top_4]: gmsh.model.mesh.setTransfiniteCurve(l, NX_COWL)
    for l in [l_cowl_back, l_top_5]: gmsh.model.mesh.setTransfiniteCurve(l, NX_WAKE)

    # --- Transfinite Settings (Y) - CLUSTERING UPDATES ---

    # 1. Ramp Boundary Layer (Stronger Clustering)
    # Increased Progression to 1.05 to pack cells harder at the wall (p1, p5, p6)
    for l in [l_inlet_bot, l_v1_bot, l_v2_bot]:
        gmsh.model.mesh.setTransfiniteCurve(l, NY_WALL, "Progression", 1.05)
    
    # 2. Freestream (Coarser)
    for l in [l_inlet_top, l_v1_top, l_v2_top, l_v3]:
        gmsh.model.mesh.setTransfiniteCurve(l, NY_FAR, "Progression", 1.02)

    # 3. Throat (Double Clustering)
    # "Bump" packs cells at BOTH ends (Top and Bottom walls)
    # 400 Cells here ensures excellent resolution for both boundary layers
    for l in [l_throat_inlet, l_out_int]:
        gmsh.model.mesh.setTransfiniteCurve(l, NY_WALL, "Bump", 0.05)

    # 4. Cowl Top (External)
    for l in [l_v4, l_out_ext]:
        gmsh.model.mesh.setTransfiniteCurve(l, NY_FAR, "Progression", 1.01)

    # Corners
    gmsh.model.mesh.setTransfiniteSurface(s1_b, cornerTags=[p1, p5, p18, p17])
    gmsh.model.mesh.setTransfiniteSurface(s2_b, cornerTags=[p5, p6, p19, p18])
    gmsh.model.mesh.setTransfiniteSurface(s3_b, cornerTags=[p6, p7, p9, p19])
    
    gmsh.model.mesh.setTransfiniteSurface(s1_t, cornerTags=[p17, p18, p13, p4])
    gmsh.model.mesh.setTransfiniteSurface(s2_t, cornerTags=[p18, p19, p14, p13])
    gmsh.model.mesh.setTransfiniteSurface(s3_t, cornerTags=[p19, p9, p15, p14])
    
    gmsh.model.mesh.setTransfiniteSurface(s4, cornerTags=[p7, p8, p10, p9])
    gmsh.model.mesh.setTransfiniteSurface(s5, cornerTags=[p9, p12, p16, p15])
    gmsh.model.mesh.setTransfiniteSurface(s6, cornerTags=[p12, p11, p3, p16])

    # --- Export ---
    all_surfaces = [s1_b, s1_t, s2_b, s2_t, s3_b, s3_t, s4, s5, s6]
    fluid = gmsh.model.addPhysicalGroup(2, all_surfaces)
    
    inlet_lines = [l_inlet_bot, l_inlet_top]
    outlet_lines = [l_out_int, l_out_ext]
    top_lines = [l_top_1, l_top_2, l_top_3, l_top_4, l_top_5]
    wall_lines = [l_wall_1, l_wall_2, l_wall_3, l_throat_bot, l_throat_top, l_cowl_top, l_cowl_back]

    gmsh.model.setPhysicalName(2, fluid, "fluid")
    gmsh.model.setPhysicalName(1, gmsh.model.addPhysicalGroup(1, inlet_lines), "inlet")
    gmsh.model.setPhysicalName(1, gmsh.model.addPhysicalGroup(1, outlet_lines), "outlet")
    gmsh.model.setPhysicalName(1, gmsh.model.addPhysicalGroup(1, top_lines), "top")
    gmsh.model.setPhysicalName(1, gmsh.model.addPhysicalGroup(1, wall_lines), "wall")

    gmsh.option.setNumber("Mesh.RecombineAll", 1)
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()
    gmsh.finalize()

if __name__ == "__main__":
    main()