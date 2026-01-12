import gmsh

def main():
    gmsh.initialize()
    gmsh.model.add("flatplate")

    lc = 0.01
    l_domain = 2.0
    h_domain = 1.0
    l_plate = 1.0
    h_plate = 0.2
    x_start = (l_domain - l_plate) / 2
    y_start = (h_domain - h_plate) / 2

    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(l_domain, 0, 0, lc)
    p3 = gmsh.model.geo.addPoint(l_domain, h_domain, 0, lc)
    p4 = gmsh.model.geo.addPoint(0, h_domain, 0, lc)

    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4)
    l4 = gmsh.model.geo.addLine(p4, p1)

    p5 = gmsh.model.geo.addPoint(x_start, y_start, 0, lc / 10)
    p6 = gmsh.model.geo.addPoint(x_start + l_plate, y_start, 0, lc / 10)
    p7 = gmsh.model.geo.addPoint(x_start + l_plate, y_start + h_plate, 0, lc / 10)
    p8 = gmsh.model.geo.addPoint(x_start, y_start + h_plate, 0, lc / 10)

    l5 = gmsh.model.geo.addLine(p5, p6)
    l6 = gmsh.model.geo.addLine(p6, p7)
    l7 = gmsh.model.geo.addLine(p7, p8)
    l8 = gmsh.model.geo.addLine(p8, p5)

    cl_domain = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4])
    cl_plate = gmsh.model.geo.addCurveLoop([l5, l6, l7, l8])

    _s1 = gmsh.model.geo.addPlaneSurface([cl_domain, cl_plate])

    gmsh.model.geo.synchronize()

    walls = [l5, l6, l7, l8]

    dist = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(dist, "CurvesList", walls)

    thresh = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(thresh, "InField", dist)
    gmsh.model.mesh.field.setNumber(thresh, "SizeMin", 0.02)
    gmsh.model.mesh.field.setNumber(thresh, "SizeMax", 0.2)
    gmsh.model.mesh.field.setNumber(thresh, "DistMin", 0.1)
    gmsh.model.mesh.field.setNumber(thresh, "DistMax", 0.5)
    gmsh.model.mesh.field.setAsBackgroundMesh(thresh)

    bl = gmsh.model.mesh.field.add("BoundaryLayer")
    gmsh.model.mesh.field.setNumbers(bl, "CurvesList", walls)
    gmsh.model.mesh.field.setNumber(bl, "Size", 0.005)
    gmsh.model.mesh.field.setNumber(bl, "Ratio", 1.1)
    gmsh.model.mesh.field.setNumber(bl, "Thickness", 0.1)
    gmsh.model.mesh.field.setNumber(bl, "Quads", 1)
    gmsh.model.mesh.field.setNumbers(bl, "FanPointsList", [p5, p6, p7, p8])
    gmsh.model.mesh.field.setNumbers(bl, "FanPointsSizesList", [4, 4, 4, 4])

    gmsh.model.mesh.field.setAsBoundaryLayer(bl)

    gmsh.option.setNumber("Mesh.Algorithm", 6)

    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()
    gmsh.finalize()

if __name__ == "__main__":
    main()