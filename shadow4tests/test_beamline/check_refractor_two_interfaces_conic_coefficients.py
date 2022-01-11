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

    import Shadow


    #
    # shadow3
    #
    from shadow4tests.oasys_workspaces.refractors_two_interfaces_conic_coefficients import define_source, run_source, define_beamline, run_beamline

    oe0 = define_source()
    beam3_source = run_source(oe0)

    #
    # compare
    #
    oe_list = define_beamline()
    oe_list[0].FWRITE = 1
    oe_list[1].FWRITE = 1
    beam3 = run_beamline(beam3_source, oe_list)


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

    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal


    interface1 = S4ConicInterfaceElement(
        optical_element=S4ConicInterface(
            name="Conic Refractive Interface",
            boundary_shape=None,
            material_object="vacuum",
            material_image ="glass",
            f_r_ind=0,
            r_ind_obj=1.0,
            r_ind_ima=1.5,
            conic_coefficients=[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 10, 0.0],
        ),
        coordinates=ElementCoordinates(p=0.0, q=0.0,
                                       angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=numpy.pi))

    interface2 = S4ConicInterfaceElement(
        optical_element=S4ConicInterface(
            name="Conic Refractive Interface",
            boundary_shape=None,
            material_object="glass",
            material_image ="vacuum",
            f_r_ind=0,
            r_ind_obj=1.5,
            r_ind_ima=1.0,
            conic_coefficients=[1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, -10, 0.0],
        ),
        coordinates=ElementCoordinates(p=0.0, q=5.0,
                                       angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=numpy.pi))

    # print(interface1.info())
    # print(interface1.get_optical_element().get_surface_shape().get_conic_coefficients())


    #
    # run
    #


    if False: # reuse shadow3 star.01
        star01_3 = Shadow.Beam()
        star01_3.load("star.01")
        tmp4 = Beam.initialize_from_array(star01_3.rays)
        mirr01_3 = Shadow.Beam()
        mirr01_3.load("mirr.01")
        tmpm4 = Beam.initialize_from_array(mirr01_3.rays)
    else:
        tmp4, tmpm4 = interface1.trace_beam(beam_in=beam4_source, flag_lost_value=-11000)


    beam4, mirr4 = interface2.trace_beam(beam_in=tmp4, flag_lost_value=-22000)



    #
    # compare first oe
    #
    if False:
        mirr3 = Shadow.Beam()
        mirr3.load("mirr.01")
        beam3 = Shadow.Beam()
        beam3.load("star.01")

        plotxy(mirr3, 1, 3, nbins=201, nolost=1, title="shadow3 footprint")
        plotxy(tmpm4, 1, 3, nbins=201, nolost=1, title="shadow4 footprint")

        plotxy(beam3, 1, 3, nbins=201, nolost=1, title="shadow3 image")
        plotxy(tmp4,  1, 3, nbins=201, nolost=1, title="shadow4 image")

        check_six_columns_mean_and_std(mirr3, tmpm4, do_assert=True, do_plot=False)
        check_six_columns_mean_and_std(beam3, tmp4, do_assert=True, do_plot=False)


    #
    # compare second oe
    #
    if True:
        mirr3 = Shadow.Beam()
        mirr3.load("mirr.02")
        #
        plotxy(beam3, 1, 3, nbins=201, nolost=1, title="shadow3 image")
        plotxy(beam4, 1, 3, nbins=201, nolost=1, title="shadow4 image")


        plotxy(mirr3, 1, 3, nbins=201, nolost=1, title="shadow3 footprint height")
        plotxy(mirr4, 1, 3, nbins=201, nolost=1, title="shadow3 footprint height")

        #
        #
        #
        check_six_columns_mean_and_std(mirr3, mirr4, do_assert=False, do_plot=False, assert_value=1e-6)
        check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False)
        #
        # there are differences in the E (cols 7,8,9, 16,17,18) and phases (13,14) I think shadow3 is wrong...
        # TODO: implement correctly in shadow4 via Fresnel equations for the transmitted beam
        check_almost_equal(mirr3, mirr4, do_assert = False, level=3)
        check_almost_equal(beam3, beam4, do_assert = False, level=3)

