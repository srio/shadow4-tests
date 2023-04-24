import numpy
from srxraylib.plot.gol import plot, set_qt

set_qt()

filename = "matsuyama_tolerances_rot_m1.dat"
a = numpy.loadtxt(filename)
filename = "matsuyama_tolerances_rot_beam.dat"
b = numpy.loadtxt(filename)
plot(a[:, 0], a[:, 1],
     b[:, 0], b[:, 1], legend=["M1","beam"])