import numpy

from shadow4.sources.source_geometrical.source_geometrical import SourceGeometrical

from shadow4.beamline.optical_elements.ideal_elements.s4_empty import S4EmptyElement


import Shadow
from Shadow.ShadowTools import plotxy
from shadow4tests.compatibility.beam3 import Beam3

from numpy.testing import assert_almost_equal

from shadow4tests.compatibility.global_definitions import SHADOW3_BINARY



class FakeOE():
    pass

def test_empty_element( do_plot=0,
                        do_assert = True,
                        do_shadow3_fortran = True,
                        N = 1000,
                        alpha_deg  = None, # 20,    # None=rondomize
                        theta1_deg = None, # 10.0,  # None=rondomize
                        theta2_deg = None, # 170.0,  # None=rondomize
                        p          = None, # 15.0,  # None=rondomize
                        q          = None, # 100.0  # None=rondomize,
                        ):


    source = SourceGeometrical()
    source.set_angular_distribution_gaussian(1e-6,1e-6)
    beam0 = source.calculate_beam(N=N, POL_DEG=1)
    print(beam0.info())


    beam0s3 = Beam3.initialize_from_shadow4_beam(beam0)

    beam1s3 = Beam3.initialize_from_shadow4_beam(beam0)


    if alpha_deg is None: alpha_deg = numpy.random.random() * 360.0
    if theta1_deg is None: theta1_deg = numpy.random.random() * 90.0
    if theta2_deg is None: theta2_deg = numpy.random.random() * 180.0
    if p is None: p = numpy.random.random() * 100.0
    if q is None: q = numpy.random.random() * 100.0


    #
    # shadow4
    #

    empty = S4EmptyElement()
    empty.get_coordinates().set_positions(angle_radial=theta1_deg*numpy.pi/180,
                     angle_radial_out=theta2_deg*numpy.pi/180,
                     angle_azimuthal=alpha_deg*numpy.pi/180, p=p, q=q)

    beam1, mirr1 = empty.trace_beam(beam0)

    #
    # shadow3
    #
    oe1 = Shadow.OE()
    oe1.ALPHA = alpha_deg
    oe1.DUMMY = 100.0
    oe1.FWRITE = 0 # 1
    oe1.F_REFRAC = 2
    oe1.T_IMAGE = q
    oe1.T_INCIDENCE = theta1_deg
    oe1.T_REFLECTION = theta2_deg
    oe1.T_SOURCE = p

    if do_shadow3_fortran:
        import os
        os.system("/bin/rm begin.dat start.01 star.01")

        beam0s3.write("begin.dat")
        oe1.write("start.01")
        f = open("systemfile.dat","w")
        f.write("start.01\n")
        f.close()
        f = open("shadow3.inp","w")
        f.write("trace\nsystemfile\n0\nexit\n")
        f.close()

        os.system("%s < shadow3.inp" % SHADOW3_BINARY)

        beam1f = Beam3(N=N)
        beam1f.load("star.01")

    beam1s3.traceOE(oe1,1)

    if do_plot:
        plotxy(beam1, 4, 6, title="Image shadow4", nbins=201)
        plotxy(beam1s3, 4, 6, title="Image shadow3", nbins=201)

    print("alpha_deg, theta1_deg, theta2_deg = ",alpha_deg, theta1_deg, theta2_deg)
    print("p, q = ", p, q)
    print("\ncol#   shadow4  shadow3 (shadow3_fortran) (source)")
    for i in range(18):
        if do_shadow3_fortran:
            print("col%d   %f  %f  %f  %f " % (i + 1, beam1.rays[0, i], beam1s3.rays[0, i],
                                               beam1f.rays[0, i], beam0s3.rays[0, i]))
        else:
            print("col%d   %f  %f  " % (i+1, beam1.rays[0,i], beam1s3.rays[0,i]))

        if do_assert:
            assert_almost_equal (beam1.rays[:,i], beam1s3.rays[:,i], 4)


if __name__ == "__main__":

    # a first test with plots
    test_empty_element(do_plot=False,
                        do_assert = True,
                        do_shadow3_fortran = True,
                        N = 1000,
                        alpha_deg=20,
                        theta1_deg = 10.0,
                        theta2_deg = 170.0,
                        p = 15.0,
                        q = 100.0)

    # 10 random tests
    for i in range(10):
        test_empty_element(do_plot=0,
                            do_assert = True,
                            do_shadow3_fortran = True,
                            N = 1000,
                            alpha_deg=None,
                            theta1_deg = None,
                            theta2_deg = None,
                            p = None,
                            q = None)
