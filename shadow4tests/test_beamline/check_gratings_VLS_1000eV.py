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

    from shadow4tests.oasys_workspaces.gratings_VLS_1000eV import define_source, run_source, define_beamline, \
            run_beamline, run_beamline2


    oe0 = define_source()
    oe_list = define_beamline()

    # store variables before running (as variables are changed!!)
    ruling = oe_list[-1].RULING
    ruling_coeff_linear = oe_list[-1].RUL_A1
    ruling_coeff_quadratic = oe_list[-1].RUL_A2
    ruling_coeff_cubic = oe_list[-1].RUL_A3
    order = oe_list[-1].ORDER
    p = oe_list[-1].T_SOURCE
    q = oe_list[-1].T_IMAGE
    angle_radial = oe_list[-1].T_INCIDENCE * numpy.pi / 180
    angle_radial_out= oe_list[-1].T_REFLECTION * numpy.pi / 180


    beam3_source = run_source(oe0)
    beam3 = run_beamline(beam3_source, oe_list)
    beam3_beforeVLS = run_beamline2(beam3_source, oe_list)
    #
    # shadow4
    #

    from shadow4.syned.element_coordinates import ElementCoordinates


    beam4_source = Beam.initialize_from_array(beam3_beforeVLS.rays)
    beam4 = beam4_source

    oe = oe_list[-1]
    check_congruence(oe)

    #
    # shadow definitions
    #

    name = "VLS Grating"

    #
    # grating
    #
    from shadow4.beamline.optical_elements.gratings.s4_plane_grating import S4PlaneGrating, S4PlaneGratingElement

    g = S4PlaneGrating(
        name = name,
        boundary_shape = None, # BoundaryShape(),
        ruling = ruling,
        ruling_coeff_linear = ruling_coeff_linear,
        ruling_coeff_quadratic = ruling_coeff_quadratic,
        ruling_coeff_cubic = ruling_coeff_cubic,
        ruling_coeff_quartic = 0,
        coating = None,
        coating_thickness = None,
        f_central=False,
        f_phot_cent=0,
        phot_cent=8000.0,
        material_constants_library_flag=0,  # 0=xraylib, 1=dabax, 2=shadow preprocessor
        file_refl="",
        order=order,
        f_ruling=5,
        )

    coordinates_syned = ElementCoordinates(p = p,
                                           q = q,
                                           angle_radial = angle_radial,
                                           angle_radial_out= angle_radial_out,
                                           angle_azimuthal = 0.0)



    ge = S4PlaneGratingElement(optical_element=g, coordinates=coordinates_syned)

    print(ge.info())
    #
    beam4, mirror4 = ge.trace_beam(beam4)
    #
    # # plotxy(beam_out[0], 1, 3, title="Image 0", nbins=201)

    #
    # compare
    #
    # oe_list = define_beamline()
    # beam3 = run_beamline(beam3_source, oe_list)

    plotxy(beam3, 1, 3, nbins=101, nolost=1, title="%s shadow3" % name)
    plotxy(beam4, 1, 3, nbins=101, nolost=1, title="%s shadow4" % name)
    #
    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal
    #
    check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False, assert_value=2e-6)
    check_almost_equal(beam3, beam4, do_assert=True, level=3, skip_columns=[7,8,9,13,14,17,18])
    # #
    # print(g.get_optical_surface_instance().ccc)

    print(">>>>>>>>>>> RULIG: ", oe.RULING, len(oe_list), oe_list[-1])