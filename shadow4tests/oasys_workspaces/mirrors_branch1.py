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

    oe0.FDISTR = 3
    oe0.HDIV1 = 0.0
    oe0.HDIV2 = 0.0
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.ISTAR1 = 5676561
    oe0.NPOINT = 100000
    oe0.PH1 = 1.0
    oe0.SIGDIX = 1e-06
    oe0.SIGDIZ = 1e-06
    oe0.SIGMAX = 0.0
    oe0.SIGMAZ = 0.0
    oe0.VDIV1 = 0.0
    oe0.VDIV2 = 0.0

    return oe0
    
def run_source(oe0, iwrite=False):
    # iwrite (1) or not (0) SHADOW files start.xx end.xx star.xx

    #Run SHADOW to create the source

    if iwrite:
        oe0.write("start.00")

    beam = Shadow.Beam()
    beam.genSource(oe0)

    if iwrite:
        oe0.write("end.00")
        beam.write("begin.dat")

    return beam


def define_beamline():
    # initialize elements
    oe_list = []

    
    oe1 = Shadow.OE()
    oe_list.append(oe1)
    oe2 = Shadow.OE()
    oe_list.append(oe2)

    # Define variables. See https://raw.githubusercontent.com/oasys-kit/shadow3/master/docs/oe.nml


    oe1.DUMMY = 100.0
    oe1.FHIT_C = 1
    oe1.FWRITE = 1
    oe1.RLEN1 = 5e-05
    oe1.RLEN2 = 5e-05
    oe1.RWIDX1 = 2e-05
    oe1.RWIDX2 = 2e-05
    oe1.T_IMAGE = 6.0
    oe1.T_INCIDENCE = 88.8
    oe1.T_REFLECTION = 88.8

    oe2.DUMMY = 100.0
    oe2.FHIT_C = 1
    oe2.FWRITE = 1
    oe2.RLEN1 = 0.00015
    oe2.RLEN2 = 0.00015
    oe2.RWIDX1 = 0.0001
    oe2.RWIDX2 = 0.0001
    oe2.T_IMAGE = 100.0
    oe2.T_INCIDENCE = 89.8281126615
    oe2.T_REFLECTION = 89.8281126615



    return oe_list

    
def run_beamline(beam_in, oe_list, iwrite=0):
    beam = beam_in.duplicate()
        
    #
    #run optical element 1
    #
    print("    Running optical element: %d"%(1))
    oe1 = oe_list[1-1]
    if iwrite:
        oe1.write("start.01")
    
    beam.traceOE(oe1,1)
    oe1 = oe_list[1-1]
    if iwrite:
        oe1.write("end.01")
        beam.write("star.01")

    #
    #run optical element 2
    #
    print("    Running optical element: %d"%(2))
    oe2 = oe_list[2-1]
    if iwrite:
        oe2.write("start.02")
    
    beam.traceOE(oe2,2)
    oe2 = oe_list[2-1]
    if iwrite:
        oe2.write("end.02")
        beam.write("star.02")

    return beam

#
# main
#

oe0 = define_source()

beam = run_source(oe0, iwrite=0)
    
oe_list = define_beamline()

beam = run_beamline(beam, oe_list, iwrite=0)

# Shadow.ShadowTools.plotxy(beam,1,3,nbins=101,nolost=1,title="Real space")
# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")
