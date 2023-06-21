#
# Python script to run shadow3. Created automatically with ShadowTools.make_python_script_from_list().
#

import Shadow
import numpy

def run_shadow(Y_ROT = 0.0001, use_ccc=None):
    # write (1) or not (0) SHADOW files start.xx end.xx star.xx
    iwrite = 0

    #
    # initialize shadow3 source (oe0) and beam
    #
    beam = Shadow.Beam()
    oe0 = Shadow.Source()
    oe1 = Shadow.OE()

    #
    # Define variables. See meaning of variables in:
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/source.nml
    #  https://raw.githubusercontent.com/srio/shadow3/master/docs/oe.nml
    #

    oe0.FDISTR = 3
    oe0.F_PHOT = 0
    oe0.HDIV1 = 0.0
    oe0.HDIV2 = 0.0
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.ISTAR1 = 5676561
    oe0.NPOINT = 50000
    oe0.PH1 = 1000.0
    oe0.SIGDIX = 1e-05
    oe0.SIGDIZ = 1e-05
    oe0.SIGMAX = 1e-06
    oe0.SIGMAZ = 1e-06
    oe0.VDIV1 = 0.0
    oe0.VDIV2 = 0.0

    if use_ccc is None:
        oe1.DUMMY = 100.0
        oe1.FMIRR = 2
        oe1.FWRITE = 1
        oe1.F_MOVE = 1
        oe1.T_IMAGE = 3.0
        oe1.T_INCIDENCE = 89.0
        oe1.T_REFLECTION = 89.0
        oe1.T_SOURCE = 30.0
        oe1.Y_ROT = Y_ROT
    else:
        oe1.CCC = use_ccc
        oe1.DUMMY = 100.0
        oe1.FMIRR = 10
        oe1.FWRITE = 1
        oe1.F_EXT = 1
        oe1.F_MOVE = 1
        oe1.T_IMAGE = 3.0
        oe1.T_INCIDENCE = 89.0
        oe1.T_REFLECTION = 89.0
        oe1.T_SOURCE = 30.0
        oe1.Y_ROT = Y_ROT

    # Run SHADOW to create the source

    if iwrite:
        oe0.write("start.00")

    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    #
    # run optical element 1
    #
    print("    Running optical element: %d" % (1))
    if iwrite:
        oe1.write("start.01")

    beam.traceOE(oe1, 1)

    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    # Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space")
    # Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
    # Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")

    return beam


import numpy as np
def rotate_and_translate_coefficients(coe_list,R_M,T):
    axx, ayy, azz, axy, ayz, axz, ax, ay, az, a0 = coe_list
    A2 = np.array([[axx,axy/2,axz/2],
        [axy/2,ayy,ayz/2],
        [axz/2,ayz/2,azz]])
    A1 = np.array([ax,ay,az])
    A0 = a0
    B2 = np.dot(R_M, np.dot(A2,R_M.T)) # first equation 6.29
    B1 = np.dot(R_M, A1) - 2 * np.dot(B2,T) # 2nd equation 6.29
    B0 = A0 + np.dot(T.T, (np.dot(B2, T) - \
        np.dot(R_M, A1))) # 3rd equation 6.29
    return np.array([ B2[0,0], B2[1,1], B2[2,2],
        B2[0,1] + B2[1,0], B2[1,2] + B2[2,1], B2[0,2] + B2[2,0],
        B1[0], B1[1], B1[2], B0])

def matrix_rot_y(Theta):
    return np.array([
                    [np.cos(Theta), 0, np.sin(Theta)],
                    [0, 1, 0],
                    [-np.sin(Theta), 0, np.cos(Theta)]])


if __name__ == "__main__":

    yaw = numpy.linspace(0.001, 0.030, 20) # in degrees
    sigma_x = numpy.zeros_like(yaw)
    sigma_z = numpy.zeros_like(yaw)

    for i in range(yaw.size):
        # # shadow internal calculation and rotaion
        # beam = run_shadow(Y_ROT=yaw[i], use_ccc=None)


        # # shadow ccc internal rotation
        # ccc = numpy.array([36.4793, 0.0111111, 36.4719, 0.0, 1.04164, 0.0, 0.0, 0.0, -6.9453, 0.0])
        # beam = run_shadow(Y_ROT=yaw[i], use_ccc=ccc)


        # using rotated ccc
        ccc0 = numpy.array([36.4793, 0.0111111, 36.4719, 0.0, 1.04164, 0.0, 0.0, 0.0, -6.9453, 0.0])
        ccc = rotate_and_translate_coefficients(ccc0, matrix_rot_y(np.radians(yaw[i])), np.array([0,0,0]))
        beam = run_shadow(Y_ROT=0, use_ccc=ccc)


        # Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space")
        x = beam.getshonecol(1)
        z = beam.getshonecol(3)
        sigma_x[i] = 1e6 * x.std()
        sigma_z[i] = 1e6 * z.std()

        print("Sigma X, Z [um]: ", 1e6*x.std(), 1e6*z.std(), )

    from srxraylib.plot.gol import plot
    plot(1e3*yaw, 100*(sigma_x-0.1)/0.1,
         1e3*yaw, 100*(sigma_z-0.1)/0.1,
         legend=['Horizontal','Vertical'], ylog=0,
         xtitle=r'yaw angle $\delta$ [mdeg]', ytitle="Relative Increase of r.m.s. size [%]", yrange=[-2.5,100])

    for i in range(yaw.size):
        print(yaw[i]*1e3, 100*(sigma_x[i]-0.1)/0.1, 100*(sigma_x[i]-0.1)/0.1)