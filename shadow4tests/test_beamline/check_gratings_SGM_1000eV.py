import numpy

from srxraylib.plot.gol import set_qt

set_qt()

from shadow4.tools.graphics import plotxy

from shadow4.beamline.optical_elements.mirrors.s4_sphere_mirror import S4SphereMirror, S4SphereMirrorElement
from shadow4.syned.shape import Convexity, Direction

from shadow4.beamline.s4_optical_element import SurfaceCalculation

from shadow4.beam.beam import Beam



def check_congruence(oe):
    pass
    # assert (oe.FHIT_C == 0)
    # assert (oe.F_REFLEC == 0)
    # assert (oe.FMIRR == 1)
    # assert (oe.F_GRATING == 0)
    # assert (oe.F_CRYSTAL == 0)


if __name__ == "__main__":

    #
    # shadow3
    #

    from shadow4tests.oasys_workspaces.gratings_SGM_1000eV import define_source, run_source, define_beamline, \
            run_beamline


    oe0 = define_source()
    beam3_source = run_source(oe0)

    #
    # shadow4
    #

    from shadow4.syned.element_coordinates import ElementCoordinates

    oe = define_beamline()[0]

    beam4_source = Beam.initialize_from_array(beam3_source.rays)
    beam4 = beam4_source

    check_congruence(oe)

    #
    # shadow definitions
    #

    # if oe.F_DEFAULT == 0:
    #     p_focus = oe.SSOUR
    #     q_focus = oe.SIMAG
    #     grazing_angle = numpy.radians(90 - oe.THETA)
    # elif oe.F_DEFAULT == 1:
    #     p_focus = oe.T_SOURCE
    #     q_focus = oe.T_IMAGE
    #     grazing_angle = numpy.radians(90 - oe.T_INCIDENCE)
    #
    # is_cylinder = oe.FCYL
    #
    # if oe.CIL_ANG == 0:
    #     cylinder_direction = Direction.TANGENTIAL
    # else:
    #     cylinder_direction = Direction.SAGITTAL
    #
    # if oe.F_CONVEX == 0:
    #     convexity = Convexity.DOWNWARD
    # elif oe.F_CONVEX == 1:
    #     convexity = Convexity.UPWARD


    name = "Spherical Grating"


    #
    # grating
    #
    from shadow4.beamline.optical_elements.gratings.s4_sphere_grating import S4SphereGrating, S4SphereGratingElement

    g = S4SphereGrating(
        name = name,
        boundary_shape = None, # BoundaryShape(),
        ruling = oe.RULING,
        ruling_coeff_linear = 0,
        ruling_coeff_quadratic = 0,
        ruling_coeff_cubic = 0,
        ruling_coeff_quartic = 0,
        coating = None,
        coating_thickness = None,
        f_central=False,
        f_phot_cent=0,
        phot_cent=8000.0,
        material_constants_library_flag=0,  # 0=xraylib, 1=dabax, 2=shadow preprocessor
        file_refl="",
        order=oe.ORDER,
        #
        surface_calculation=SurfaceCalculation.EXTERNAL,
        is_cylinder=False,
        cylinder_direction=Direction.TANGENTIAL,
        convexity=Convexity.DOWNWARD,
        radius=oe.RMIRR,
        p_focus=0.0,
        q_focus=0.0,
        grazing_angle=0.0,
        )

    coordinates_syned = ElementCoordinates(p = oe.T_SOURCE,
                                           q = oe.T_IMAGE,
                                           angle_radial = oe.T_INCIDENCE * numpy.pi / 180,
                                           angle_radial_out= oe.T_REFLECTION * numpy.pi / 180,
                                           angle_azimuthal = 0.0)



    ge = S4SphereGratingElement(optical_element=g, coordinates=coordinates_syned)

    print(ge.info())

    beam4, mirror4 = ge.trace_beam(beam4)

    # plotxy(beam_out[0], 1, 3, title="Image 0", nbins=201)

    #
    # compare
    #
    oe_list = define_beamline()
    beam3 = run_beamline(beam3_source, oe_list)

    plotxy(beam3, 1, 3, nbins=101, nolost=1, title="%s shadow3" % name)
    plotxy(beam4, 1, 3, nbins=101, nolost=1, title="%s shadow4" % name)

    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal

    check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False, assert_value=1e-6)
    check_almost_equal(beam3, beam4, do_assert=True, level=3, skip_columns=[13])

    print(g.get_optical_surface_instance().ccc)