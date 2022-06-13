def check_congruence(oe):

    assert (oe.F_CRYSTAL == 1)
    assert (oe.DUMMY == 100.0)


if __name__ == "__main__":
    import numpy

    from srxraylib.plot.gol import set_qt
    set_qt()

    from shadow4.tools.graphics import plotxy
    from shadow4.beam.beam import Beam


    #
    # shadow3
    #
    from shadow4tests.oasys_workspaces.crystal_diff_profile_vs_angle import define_source, run_source, define_beamline, run_beamline

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

    from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystal
    from shadow4.beamline.optical_elements.crystals.s4_plane_crystal import S4PlaneCrystalElement

        # refractors.s4_conic_interface import S4ConicInterface, \
        # S4ConicInterfaceElement

    from shadow4.tools.graphics import plotxy

    from shadow4.syned.element_coordinates import ElementCoordinates

    from syned.beamline.optical_elements.crystals.crystal import DiffractionGeometry

    crystal1 = S4PlaneCrystalElement(
                                optical_element=S4PlaneCrystal(
                                    name="Plane crystal",
                                    boundary_shape=None,
                                    material="Si",
                                    diffraction_geometry=DiffractionGeometry.BRAGG,  # ?? not supposed to be in syned...
                                    miller_index_h=1,
                                    miller_index_k=1,
                                    miller_index_l=1,
                                    asymmetry_angle=0.0,
                                    thickness=0.010,  ###########################
                                    f_central=True,
                                    f_phot_cent=0,
                                    phot_cent=8000.0,
                                    file_refl="Si5_15.111",
                                    f_bragg_a=False,
                                    # a_bragg=0.0,
                                    f_johansson=False,
                                    r_johansson=1.0,
                                    f_mosaic=False,
                                    spread_mos=0.4 * numpy.pi / 180,
                                    f_ext=0,
                                    material_constants_library_flag=0,
                                ),
                                coordinates=ElementCoordinates(p=5.0, q=0.010,
                                            angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=0.0))


    # crystal1 = S4PlaneCrystal(            name="Undefined",
    #         boundary_shape=None,
    #         material="Si",
    #         diffraction_geometry=DiffractionGeometry.BRAGG, #?? not supposed to be in syned...
    #         miller_index_h=1,
    #         miller_index_k=1,
    #         miller_index_l=1,
    #         asymmetry_angle=0.0,
    #         thickness=0.010, ###########################
    #         f_central=1,
    #         f_phot_cent=0,
    #         phot_cent=8000.0,
    #         file_refl="",
    #         f_bragg_a=False,
    #         # a_bragg=0.0,
    #         f_johansson=False,
    #         r_johansson=1.0,
    #         f_mosaic=False,
    #         spread_mos=0.4*numpy.pi/180,
    #         f_ext=0,)
    #
    #
    # # interface1 = S4ConicInterfaceElement(
    # optical_element=S4PlaneCrystalElement(
    #     crystal1,
    #     coordinates=ElementCoordinates(p=5.0, q=0.010,
    #                                angle_radial=0.0, angle_azimuthal=0.0, angle_radial_out=None))

    print(crystal1.info())
    # print(crystal1.get_optical_element().get_surface_shape().get_conic_coefficients())


    #
    # run
    #

    beam4, mirr4 = crystal1.trace_beam(beam_in=beam4_source, flag_lost_value=-11000)


    #
    # compare
    #
    oe_list = define_beamline()
    oe_list[0].FWRITE = 1
    beam3 = run_beamline(beam3_source, oe_list)

    plotxy(beam3, 6, 23, nbins=201, nolost=1, title="shadow3 diff profile")
    plotxy(beam4, 6, 23, nbins=201, nolost=1, title="shadow4 diff profile")
    #
    #
    #
    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal
    #
    #
    check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False)
    check_almost_equal(beam3, beam4, do_assert = False, level=3)

