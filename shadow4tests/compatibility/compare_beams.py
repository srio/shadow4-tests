"""
Tools to compare beams from shadow3 and Shadow4
"""
import numpy
from srxraylib.plot.gol import plot_scatter
import Shadow
from numpy.testing import assert_almost_equal


def check_six_columns_mean_and_std(beam3, beam4, do_plot=True, do_assert=False, assert_value=1e-2, to_meters=1.0, good_only=True):

    raysnew = beam4.rays
    rays = beam3.rays

    if good_only:
        indices = numpy.where(rays[:,9] > 0 )[0]
        print(indices)
        rays = rays[indices, :].copy()
        raysnew = raysnew[indices, :].copy()

    if do_plot:
        # plot_scatter(rays[:,1],rays[:,0],title="Trajectory shadow3",show=False)
        # plot_scatter(raysnew[:,1],raysnew[:,0],title="Trajectory shadow4")


        plot_scatter(rays[:,3],rays[:,5],title="Divergences shadow3",show=False)
        plot_scatter(raysnew[:,3],raysnew[:,5],title="Divergences shadow4")

        plot_scatter(rays[:,0],rays[:,2],title="Real Space shadow3",show=False)
        plot_scatter(raysnew[:,0],raysnew[:,2],title="Real Space shadow4")

        #
        b3 = Shadow.Beam()
        b3.rays = rays

        b4 = Shadow.Beam()
        b4.rays = raysnew
        Shadow.ShadowTools.histo1(b3,11,ref=23,nolost=1)
        Shadow.ShadowTools.histo1(b4,11,ref=23,nolost=1)



    print("Comparing...")
    for i in range(6):

        m0 = (raysnew[:,i]).mean()
        m1 = (rays[:,i]*to_meters).mean()
        print("\ncol %d, mean sh3, sh4, |sh4-sh3|: %10g  %10g  %10g"%(i+1,m1,m0,numpy.abs(m0-m1)))
        std0 = raysnew[:,i].std()
        std1 = (rays[:,i]*to_meters).std()
        print("col %d, stdv sh3, sh4, |sh4-sh3|: %10g  %10g  %10g"%(i+1,std1,std0,numpy.abs(std0-std1)))

        if do_assert:
            assert(numpy.abs(m0-m1) < assert_value)
            assert(numpy.abs(std0-std1) < assert_value)

def check_almost_equal(beam3, beam4, do_assert=True, display_ray_number=10, level=1):

    print("\ncol#   shadow3  shadow4")
    for i in range(18):

        print("col%d   %20.10f  %20.10f  " % (i + 1, beam3.rays[display_ray_number, i], beam4.rays[display_ray_number, i]))
        if do_assert:
            if i in [13,14]: # angles
                assert_almost_equal( numpy.mod(beam3.rays[:, i], numpy.pi), numpy.mod(beam4.rays[:, i], numpy.pi), level)
            else:
                assert_almost_equal (beam3.rays[:,i], beam4.rays[:,i], level)