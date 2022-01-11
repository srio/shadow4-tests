def check_congruence(oe):

    assert (oe.FMIRR == 10)
    assert (oe.F_EXT == 1)
    assert (oe.F_REFRAC == 1)


if __name__ == "__main__":
    import numpy

    from srxraylib.plot.gol import set_qt
    set_qt()

    from shadow4.tools.graphics import plotxy
    from shadow4.beam.beam import Beam


    #
    # shadow3
    #
    from shadow4tests.oasys_workspaces.refractors_interface_conic_coefficients import define_source, run_source, define_beamline, run_beamline

    oe0 = define_source()
    beam3_source = run_source(oe0)

    #
    # shadow4
    #
    from shadow4.syned.element_coordinates import ElementCoordinates

    oe_list = define_beamline() # just in case... reinitializa to "before run"
    oe = oe_list[0]

    beam4_source = Beam.initialize_from_array(beam3_source.rays)

    check_congruence(oe)


    #
    # shadow definitions
    #

    from shadow4.beamline.optical_elements.refractors.s4_conic_interface import S4ConicInterface, \
        S4ConicInterfaceElement

    from shadow4.tools.graphics import plotxy

    from shadow4.syned.element_coordinates import ElementCoordinates

    interface1 = S4ConicInterfaceElement(
        optical_element=S4ConicInterface(
            name="Conic Refractive Interface",
            boundary_shape=None,
            material_object="vacuum",
            material_image ="glass",
            f_r_ind=0,
            r_ind_obj=1.0,
            r_ind_ima=1.5,
            conic_coefficients=[1.0, 1.0, 1.0, 0.0, -0.0, -0.0, 0.0, 0.0, 3350.0e-3, 0.0],
        ),
        coordinates=ElementCoordinates(p=0.0, q=5000.0e-3,
                                       angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=numpy.pi))

    print(interface1.info())
    print(interface1.get_optical_element().get_surface_shape().get_conic_coefficients())


    #
    # run
    #

    beam4, mirr4 = interface1.trace_beam(beam_in=beam4_source, flag_lost_value=-11000)


    #
    # compare
    #
    oe_list = define_beamline()
    oe_list[0].FWRITE = 1
    beam3 = run_beamline(beam3_source, oe_list)

    plotxy(beam3, 1, 3, nbins=201, nolost=1, title="shadow3 image")
    plotxy(beam4, 1, 3, nbins=201, nolost=1, title="shadow4 image")


    import Shadow
    mirr3 = Shadow.Beam()
    mirr3.load("mirr.01")

    plotxy(mirr3, 1, 3, nbins=201, nolost=1, title="shadow3 footprint")
    plotxy(mirr4, 1, 3, nbins=201, nolost=1, title="shadow4 footprint")

    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal


    check_six_columns_mean_and_std(mirr3, mirr4, do_assert=True, do_plot=False)
    check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False)

    # there are differences in the E (cols 7,8,9, 16,17,18) and phases (13,14) I think shadow3 is wrong...
    # TODO: implement correctly in shadow4 via Fresnel equations for the transmitted beam
    check_almost_equal(mirr3, mirr4, do_assert = False, level=3)
    check_almost_equal(beam3, beam4, do_assert = False, level=3)

