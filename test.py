import gmsh


def main():
    gmsh.initialize()

    lc = 0.1
    l_domain = 2.0
    h_domain = 1.0
    w_start = 0.5
    w_length = 1.0
    w_height = 0.3

    p1 = gmsh.model.geo.addPoint(0, 0, 0, lc)
    p2 = gmsh.model.geo.addPoint(w_start, 0, 0, lc) 
    p3 = gmsh.model.geo.addPoint(w_start + w_length/2, w_height, 0, lc)
    p4 = gmsh.model.geo.addPoint(w_start + w_length, 0, 0, lc)
    p5 = gmsh.model.geo.addPoint(l_domain, 0, 0, lc)
    p6 = gmsh.model.geo.addPoint(l_domain, h_domain, 0, lc)
    p7 = gmsh.model.geo.addPoint(0, h_domain, 0, lc)

    l1 = gmsh.model.geo.addLine(p1, p2)
    l2 = gmsh.model.geo.addLine(p2, p3)
    l3 = gmsh.model.geo.addLine(p3, p4) 
    l4 = gmsh.model.geo.addLine(p4, p5)
    l5 = gmsh.model.geo.addLine(p5, p6)
    l6 = gmsh.model.geo.addLine(p6, p7) 
    l7 = gmsh.model.geo.addLine(p7, p1) 

    cl = gmsh.model.geo.addCurveLoop([l1, l2, l3, l4, l5, l6, l7])
    s = gmsh.model.geo.addPlaneSurface([cl])

    gmsh.model.geo.synchronize()

    walls = [l1, l2, l3, l4]

    bl = gmsh.model.mesh.field.add("BoundaryLayer")
    gmsh.model.mesh.field.setNumbers(bl, "CurvesList", walls)
    gmsh.model.mesh.field.setNumber(bl, "Size", 0.005)
    gmsh.model.mesh.field.setNumber(bl, "Ratio", 1.1)
    gmsh.model.mesh.field.setNumber(bl, "Thickness", 0.2)
    gmsh.model.mesh.field.setNumber(bl, "Quads", 1)
    gmsh.model.mesh.field.setNumbers(bl, "FanPointsList", [p3])
    gmsh.model.mesh.field.setAsBoundaryLayer(bl)

    gmsh.option.setNumber("Mesh.Algorithm", 6)

    gmsh.model.mesh.generate(2)
    gmsh.fltk.run()
    gmsh.finalize()


if __name__ == "__main__":
    main()