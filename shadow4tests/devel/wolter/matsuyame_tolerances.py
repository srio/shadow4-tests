#
# Python script to run shadow3. Created automatically with make_python_script_from_list().
#
import Shadow
import numpy


def define_source():
    #
    # initialize shadow3 source (oe0) and beam
    #
    oe0 = Shadow.Source()

    # Define variables. See https://raw.githubusercontent.com/oasys-kit/shadow3/master/docs/source.nml

    oe0.CONE_MAX = 5e-06
    oe0.FDISTR = 5
    oe0.FSOUR = 2
    oe0.F_PHOT = 0
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.ISTAR1 = 5676561
    oe0.NPOINT = 50000
    oe0.PH1 = 11500.0
    oe0.WXSOU = 1.25e-05
    oe0.WZSOU = 1.25e-05

    return oe0


def run_source(oe0, iwrite=False):
    # iwrite (1) or not (0) SHADOW files start.xx end.xx star.xx

    # Run SHADOW to create the source

    if iwrite:
        oe0.write("start.00")

    beam = Shadow.Beam()
    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    return beam


def define_beamline(X_ROT=0.0):
    # initialize elements
    oe_list = []

    oe1 = Shadow.OE()
    oe_list.append(oe1)
    oe2 = Shadow.OE()
    oe_list.append(oe2)

    # Define variables. See https://raw.githubusercontent.com/oasys-kit/shadow3/master/docs/oe.nml

    oe1.CCC = numpy.array(
        [5846.490134625098, 0.045836362869578186, 5846.4462174678365, 0.0, 32.04741572531343, 0.0, 0.0, 0.0,
         -31.291997277978908, 0.0])
    oe1.DUMMY = 100.0
    oe1.FHIT_C = 1
    oe1.FMIRR = 10
    oe1.FWRITE = 1
    oe1.F_EXT = 1
    oe1.F_MOVE = 1
    oe1.OFFY = 2.22e-07
    oe1.RLEN1 = 0.065
    oe1.RLEN2 = 0.065
    oe1.RWIDX1 = 0.025
    oe1.RWIDX2 = 0.025
    oe1.T_IMAGE = 0.075
    oe1.T_INCIDENCE = 89.83957181736336
    oe1.T_REFLECTION = 89.83957181736336
    oe1.T_SOURCE = 45.17
    oe1.X_ROT = X_ROT

    oe2.CCC = numpy.array(
        [-1848062.737743177, -46.20118343205854, -1847960.8414621525, 0.0, -27444.927571197237, 0.0, 0.0,
         1.1510792319313623e-11, 2985.178365734318, 0.0])
    oe2.DUMMY = 100.0
    oe2.FHIT_C = 1
    oe2.FMIRR = 10
    oe2.FWRITE = 1
    oe2.F_EXT = 1
    oe2.F_MOVE = 1
    oe2.RLEN1 = 0.015
    oe2.RLEN2 = 0.015
    oe2.RWIDX1 = 0.05
    oe2.RWIDX2 = 0.05
    oe2.T_IMAGE = 0.065
    oe2.T_INCIDENCE = 89.71352110243458
    oe2.T_REFLECTION = 89.71352110243458
    oe2.T_SOURCE = 0.075
    oe2.X_ROT = 3.33e-17

    return oe_list


def run_beamline(beam_in, oe_list, iwrite=0):
    beam = beam_in.duplicate()

    #
    # run optical element 1
    #
    print("    Running optical element: %d" % (1))
    oe1 = oe_list[1 - 1]
    if iwrite:
        oe1.write("start.01")

    beam.traceOE(oe1, 1)
    oe1 = oe_list[1 - 1]
    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    #
    # run optical element 2
    #
    print("    Running optical element: %d" % (2))
    oe2 = oe_list[2 - 1]
    if iwrite:
        oe2.write("start.02")

    beam.traceOE(oe2, 2)
    oe2 = oe_list[2 - 1]
    if iwrite:
        oe2.write("end.02")
        beam.write("star.02")

    return beam


#
# main
#
if __name__ == "__main__":

    oe0 = define_source()

    beam0 = run_source(oe0, iwrite=0)

    tol_a_n = 55
    tol_a = numpy.linspace(-15e-6, 15e-6, tol_a_n)
    tol_a_deg = numpy.degrees(tol_a)

    fwhm = numpy.zeros_like(tol_a)


    for i in range(tol_a_n):
        beam = beam0.duplicate()

        oe_list = define_beamline(X_ROT=tol_a_deg[i])

        beam = run_beamline(beam, oe_list, iwrite=0)

        # Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title="Real space %f (rad)" % (tol_a[i]))
        width = 5e-6
        # Shadow.ShadowTools.histo1(beam, 3, nbins=1001, nolost=1, xrange=[-width,width])
        tkt = beam.histo1(3, nbins=101, nolost=1, xrange=[-width,width])
        fwhm[i] = tkt['fwhm']

        # print(tkt)
        # tkt = beam.histo1(1, )
    # Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
    # Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")
    from srxraylib.plot.gol import plot
    plot(tol_a, 1e9*fwhm)
    for i in range(tol_a_n):
        print(i, tol_a[i], 1e9 * fwhm[i])