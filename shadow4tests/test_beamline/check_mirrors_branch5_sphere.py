import numpy

from srxraylib.plot.gol import set_qt

set_qt()

from shadow4.tools.graphics import plotxy

from shadow4.beamline.optical_elements.mirrors.s4_sphere_mirror import S4SphereMirror, S4SphereMirrorElement
from shadow4.syned.shape import Convexity, Direction

from shadow4.beamline.s4_optical_element import SurfaceCalculation

from shadow4.beam.beam import Beam



def check_congruence(oe):

    assert (oe.FHIT_C == 0)
    assert (oe.F_REFLEC == 0)
    assert (oe.FMIRR == 1)
    assert (oe.F_GRATING == 0)
    assert (oe.F_CRYSTAL == 0)


def run_sphere(kind="sphere"):
    #
    # shadow3
    #
    if kind == "sphere":
        from shadow4tests.oasys_workspaces.mirrors_branch5_sphere import define_source, run_source, define_beamline, run_beamline
    elif kind == "sphere_tangential_cylinder":
        from shadow4tests.oasys_workspaces.mirrors_branch5_sphere_tangential_cylinder import define_source, run_source, define_beamline, run_beamline
    elif kind == "sphere_sagittal_cylinder":
        from shadow4tests.oasys_workspaces.mirrors_branch5_sphere_sagittal_cylinder import define_source, run_source, define_beamline, run_beamline
    else:
        raise Exception("Bad input")

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

    if oe.F_DEFAULT == 0:
        p_focus = oe.SSOUR
        q_focus = oe.SIMAG
        grazing_angle = numpy.radians(90 - oe.THETA)
    elif oe.F_DEFAULT == 1:
        p_focus = oe.T_SOURCE
        q_focus = oe.T_IMAGE
        grazing_angle = numpy.radians(90 - oe.T_INCIDENCE)


    is_cylinder = oe.FCYL

    if oe.CIL_ANG == 0:
        cylinder_direction = Direction.TANGENTIAL
    else:
        cylinder_direction = Direction.SAGITTAL

    if oe.F_CONVEX == 0:
        convexity = Convexity.DOWNWARD
    elif oe.F_CONVEX == 1:
        convexity = Convexity.UPWARD

    name = "Sphere Mirror (%s) " % kind
    mirror1 = S4SphereMirrorElement(
        optical_element=S4SphereMirror(
                name=name,
                boundary_shape=None,
                surface_calculation=SurfaceCalculation.INTERNAL,
                is_cylinder=is_cylinder,
                cylinder_direction=cylinder_direction,
                convexity=convexity,
                radius=0.0,
                p_focus=p_focus,
                q_focus=q_focus,
                grazing_angle=grazing_angle,

            # inputs related to mirror reflectivity
                f_reflec=oe.F_REFLEC,  # reflectivity of surface: 0=no reflectivity, 1=full polarization
                # f_refl=0,  # 0=prerefl file, 1=electric susceptibility, 2=user defined file (1D reflectivity vs angle)
                #             # 3=user defined file (1D reflectivity vs energy), # 4=user defined file (2D reflectivity vs energy and angle)
                # file_refl="",  # preprocessor file fir f_refl=0,2,3,4
                # refraction_index=1.0  # refraction index (complex) for f_refl=1
                ),
        coordinates=ElementCoordinates(
                p=oe.T_SOURCE,
                q=oe.T_IMAGE,
                angle_radial=numpy.radians(oe.T_INCIDENCE),
                ),
    )

    print(mirror1.info())

    #
    # run
    #

    beam4, mirr4 = mirror1.trace_beam(beam_in=beam4, flag_lost_value=-11000)



    #
    # compare
    #
    oe_list = define_beamline()
    beam3 = run_beamline(beam3_source, oe_list)

    plotxy(beam3, 1, 3, nbins=201, nolost=1, title="%s shadow3" % name)
    plotxy(beam4, 1, 3, nbins=201, nolost=1, title="%s shadow4" % name)

    from shadow4tests.compatibility.compare_beams import check_six_columns_mean_and_std, check_almost_equal

    check_six_columns_mean_and_std(beam3, beam4, do_assert=True, do_plot=False, assert_value=1e-6)
    check_almost_equal(beam3, beam4, do_assert = True, level=3)


if __name__ == "__main__":

    run_sphere("sphere")
    run_sphere("sphere_tangential_cylinder")
    run_sphere("sphere_sagittal_cylinder")