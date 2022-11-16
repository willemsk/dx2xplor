import os
import argparse
import gridData
import numpy as np

"""
Map header
The X-PLOR map file begins with an eight-line header.

1.   Line 1
An empty line written by the `/ ` FORTRAN format descriptor in the formatted map file.

2.   Lines 2- 5
Title information written as character strings. These lines are written as 80-character strings in the formatted file map.

3.   Line 6
A series of nine integers NA, AMIN, AMAX, NB, BMIN, BMAX, NC, CMIN, CMAX. The values NA, NB and NC indicate the total number of grid points along the a,b, and c cell edges. The items AMIN, AMAX, BMIN, BMAX, CMIN, CMAX indicate the starting and stopping grid points along each cell edge in the portion of the map that is written. In the formatted map file this line is written using the FORTRAN format statement (9I8).

4.   Line 7
A series of six double-precision items corresponding to the crystal cell dimensions a, b, c, alpha, beta, gamma. In the formatted map file these items are written using the FORTRAN format statement (6E12.5).

5.   Line 8
A three-letter character string which always reads `ZXY'.

Density array
Following the map header, the density matrix is then written section-by-section with c moving slowest (in z-sections). Each section of the density map is preceded by a section number.
Thus, for the formatted map file each section of the density map is written using FORTRAN statements of the type

WRITE(OUNIT,'(I8)') KSECT

WRITE(OUNIT,'(6E12.5)') ((SECTON(I,J),I=1,ISECT),J=1,JSECT)

and the resulting map is written with six pixels on each line. The binary format is identical except the format statements are missing, so that each line that is written contains the entire length of map along the `fast' (a-axis) direction.


Map footer
Two lines follow the density array.

1.   Line 1
The integer `-9999' is always written. For the formatted map file, The FORTRAN format statement (I8) is used to write this value.

2.   Line 2
Two double-precision items corresponding to the average electron density and the standard deviation of the map. For the formatted map file these items are written using the FORTRAN format statement (2(E12.4,1X)).
"""

"""

       1
                                                                        qdi    
     256     -74     182     256    -128     128     256     132     388
 0.12800E+03 0.12800E+03 0.12800E+03 0.90000E+02 0.90000E+02 0.90000E+02
ZYX
       0
"""

class XPLORGrid():

    def __init__(self):
        
        self.array = None
        self.offset = None
        self.spacing = None
        self.shape = None

        self.format = 'Xplor'
        self._size = None
        self._ignored_lines = None
        self._first = None
        self._last = None
        self._angles = None

    def fromDX(self, DX):

        # self._ignored_lines = DX.metadata
        self._ignored_lines = ['DX2XPLOR conversion']
        self.array = DX.grid
        
        self.spacing = DX.delta
        self.shape = DX.grid.shape

        self._size = np.array([edge[-1] - edge[0] for edge in DX.edges])

        min_corner = np.array([edge[0] for edge in DX.edges])
        
        self._first = np.array([int(si / sh * co) for si, sh, co in zip(
                            self._size, self.shape, min_corner)])
        self._last = np.array([int(si + fi) for si, fi in zip(
                            self._size, self._first)])
        self._angles = np.array([90, 90, 90])

        self.offset = (self._first - 0.5) * self.spacing

    def write(self, filename):
        """Write grid data into a file.
        If a filename is not provided, gridname_state.xplor will be used.
        """

        xplor_file = open(filename, 'w')

        for line in self._ignored_lines:
            xplor_file.write(line+'\n')
        
        xplor_file.write(('{0[0]:8d}{1[0]:8d}{2[0]:8d}'
                            '{0[1]:8d}{1[1]:8d}{2[1]:8d}'
                            '{0[2]:8d}{1[2]:8d}{2[2]:8d}\n').format(
                                            self.shape,
                                            self._first,
                                            self._last))

        xplor_file.write(('{0[0]:12.3f}{0[1]:12.3f}{0[2]:12.3f}'
                            '{1[0]:12.3f}{1[1]:12.3f}{1[2]:12.3f}\n').format(
                                                        self._size,
                                                        self._angles))
        xplor_file.write('ZYX\n')

        format_ = ''
        for i in range(self.shape[0]):
            if i != 0 and i % 6 == 0:
                format_ += '\n'
            format_ += '{0['+str(i)+']:12.5f}'
        else:
            if i % 6 != 0:
                format_ += '\n'

        for k in range(self.shape[2]):
            xplor_file.write('{0:8d}\n'.format(k + self._first[2]))
            for j in range(self.shape[1]):
                xplor_file.write(format_.format(self.array[:, j, k]))
        xplor_file.close()
        return filename



def main(infilename, outfilename):
    """[summary]

    Parameters
    ----------
    inputfile : [type]
        [description]
    outputfile : [type]
        [description]
    """

    # Load grid
    dx_grid = gridData.Grid()
    dx_grid.load(infilename)

    # Create XPLOR grid
    xplor_grid = XPLORGrid()
    xplor_grid.fromDX(dx_grid)

    # Write XPLOR file
    xplor_grid.write(outfilename)


if __name__ == '__main__':
    program_args = argparse.ArgumentParser(description='OpenDX to XPLOR Grid Converter')
    program_args.add_argument('-i', '--inputfile' , required=True,  help="Input file path")
    program_args.add_argument('-o', '--outputfile', required=False, help="Output file path")

    args = program_args.parse_args()

    if args.inputfile:
        infilename = args.inputfile
        assert ".dx" in infilename.lower(), 'unsupported file : "it supports only .DX File Format as input"'
        
    if args.outputfile:
        outfilename = args.outputfile
        assert ".xplor" in outfilename.lower(), 'unsupported file : "it supports only .XPLOR File Format as output"'

    main(infilename, outfilename)


