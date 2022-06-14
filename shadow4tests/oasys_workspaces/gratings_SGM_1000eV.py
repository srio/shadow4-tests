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
    oe0.F_COLOR = 3
    oe0.F_PHOT = 0
    oe0.F_POLAR = 0
    oe0.HDIV1 = 0.5
    oe0.HDIV2 = 0.5
    oe0.IDO_VX = 0
    oe0.IDO_VZ = 0
    oe0.IDO_X_S = 0
    oe0.IDO_Y_S = 0
    oe0.IDO_Z_S = 0
    oe0.NPOINT = 150000
    oe0.PH1 = 999.8
    oe0.PH2 = 1000.2
    oe0.SIGDIX = 2.12494e-05
    oe0.SIGDIZ = 1.77667e-05
    oe0.SIGMAX = 0.000279
    oe0.SIGMAZ = 1.53882e-05
    oe0.VDIV1 = 0.5
    oe0.VDIV2 = 0.5

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

    # Define variables. See https://raw.githubusercontent.com/oasys-kit/shadow3/master/docs/oe.nml


    oe1.DUMMY = 100.0
    oe1.FMIRR = 1
    oe1.F_EXT = 1
    oe1.F_GRATING = 1
    oe1.ORDER = 1.0
    oe1.RMIRR = 635.757
    oe1.RULING = 800000.0
    oe1.T_IMAGE = 9.93427
    oe1.T_INCIDENCE = 87.29533343
    oe1.T_REFLECTION = 89.10466657
    oe1.T_SOURCE = 30.0



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

    return beam

#
# main
#

oe0 = define_source()

beam = run_source(oe0, iwrite=1)
    
oe_list = define_beamline()

beam = run_beamline(beam, oe_list, iwrite=1)

Shadow.ShadowTools.plotxy(beam,1,3,nbins=101,nolost=1,title="Real space")
# Shadow.ShadowTools.plotxy(beam,1,4,nbins=101,nolost=1,title="Phase space X")
# Shadow.ShadowTools.plotxy(beam,3,6,nbins=101,nolost=1,title="Phase space Z")
