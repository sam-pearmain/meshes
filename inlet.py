import gmsh
from math import radians, tan

L0 = 150

DOMAIN_LENGTH, DOMAIN_HEIGHT = 1.04 * L0, 0.4 * L0
INTAKE_LENGTH, INTAKE_HEIGHT = 150.0, 44.0
THROAT_HEIGHT, RAMP_LENGTH = 15.0, 81.7
RAMP_HEIGHT = 21.0
RAMP_ANGLE_ONE, RAMP_ANGLE_TWO = 10.0, 22.0
COWL_ANGLE, COWL_HEIGHT = 30.0, 8.0

KINK_LENGTH = (RAMP_HEIGHT - tan(radians(RAMP_ANGLE_TWO)) * RAMP_LENGTH) / (
    tan(radians(RAMP_ANGLE_ONE)) - tan(radians(RAMP_ANGLE_TWO))
)
KINK_HEIGHT = tan(radians(RAMP_ANGLE_ONE)) * KINK_LENGTH


LC = 0.8
BL_THICKNESS = 4.0
BL_LMIN = 0.1

def main():
    gmsh.initialize()
    gmsh.model.add("inlet")

    # domain bounds
    p1 = gmsh.model.geo.addPoint(0, 0, 0, LC)
    _p2 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, 0, 0, LC)
    p3 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, DOMAIN_HEIGHT, 0, LC)
    p4 = gmsh.model.geo.addPoint(0, DOMAIN_HEIGHT, 0, LC)

    # ramp points
    p5 = gmsh.model.geo.addPoint(DOMAIN_LENGTH - INTAKE_LENGTH, 0, 0, LC)
    p6 = gmsh.model.geo.addPoint(
        DOMAIN_LENGTH - INTAKE_LENGTH + KINK_LENGTH, KINK_HEIGHT, 0, LC
    )
    p7 = gmsh.model.geo.addPoint(
        DOMAIN_LENGTH - INTAKE_LENGTH + RAMP_LENGTH, RAMP_HEIGHT, 0, LC
    )
    p8 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, RAMP_HEIGHT, 0, LC)

    # cowl points
    p9 = gmsh.model.geo.addPoint(
        DOMAIN_LENGTH - INTAKE_LENGTH + RAMP_LENGTH, RAMP_HEIGHT + THROAT_HEIGHT, 0, LC
    )
    p10 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, RAMP_HEIGHT + THROAT_HEIGHT, 0, LC)
    p11 = gmsh.model.geo.addPoint(DOMAIN_LENGTH, INTAKE_HEIGHT, 0, LC)
    p12 = gmsh.model.geo.addPoint(
        DOMAIN_LENGTH
        - INTAKE_LENGTH
        + RAMP_LENGTH
        + (COWL_HEIGHT / tan(radians(COWL_ANGLE))),
        INTAKE_HEIGHT,
        0,
        LC,
    )

    # lines
    l1: int = gmsh.model.geo.addLine(p1, p5)
    l2: int = gmsh.model.geo.addLine(p5, p6)
    l3: int = gmsh.model.geo.addLine(p6, p7)
    l4: int = gmsh.model.geo.addLine(p7, p8)
    l5: int = gmsh.model.geo.addLine(p8, p10)
    l6: int = gmsh.model.geo.addLine(p10, p9)
    l7: int = gmsh.model.geo.addLine(p9, p12)
    l8: int = gmsh.model.geo.addLine(p12, p11)
    l9: int = gmsh.model.geo.addLine(p11, p3)
    l10: int = gmsh.model.geo.addLine(p3, p4)
    l11: int = gmsh.model.geo.addLine(p4, p1)

    # curve and plane
    cl1: int = gmsh.model.geo.addCurveLoop(
        [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11]
    )
    _plane: int = gmsh.model.geo.addPlaneSurface([cl1])
    walls = [l1, l2, l3, l4]

    gmsh.model.geo.synchronize()

    # distance field
    distance: int = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(distance, "CurvesList", walls)

    # threshold field
    threshold: int = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(threshold, "InField", distance)
    gmsh.model.mesh.field.setNumber(threshold, "SizeMin", 0.5)
    gmsh.model.mesh.field.setNumber(threshold, "SizeMax", LC)
    gmsh.model.mesh.field.setNumber(threshold, "DistMin", BL_THICKNESS)
    gmsh.model.mesh.field.setNumber(threshold, "DistMax", BL_THICKNESS + 20)
    gmsh.model.mesh.field.setAsBackgroundMesh(threshold)

    # boundary field
    boundary = gmsh.model.mesh.field.add("BoundaryLayer")
    gmsh.model.mesh.field.setNumbers(boundary, "CurvesList", walls)
    gmsh.model.mesh.field.setNumber(boundary, "Size", BL_LMIN)
    gmsh.model.mesh.field.setNumber(boundary, "Ratio", 1.2)
    gmsh.model.mesh.field.setNumber(boundary, "Thickness", BL_THICKNESS)
    gmsh.model.mesh.field.setNumber(boundary, "Quads", 1)
    gmsh.model.mesh.field.setNumbers(boundary, "PointsList", [p9])
    gmsh.model.mesh.field.setAsBoundaryLayer(boundary)

    # meshing algorithm
    gmsh.option.setNumber("Mesh.Algorithm", 6)

    # generate
    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()
    gmsh.finalize()


if __name__ == "__main__":
    main()

