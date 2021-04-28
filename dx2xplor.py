import os
import argparse
import gridData

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

 def _export_xplor(grid, filename, type=None, typequote='"', **kwargs):
        """Export the density grid to an XPLOR file.

        The file format is the simplest regular grid array and it is
        also understood by VMD's and Chimera's DX reader; PyMOL
        requires the dx `type` to be set to "double".

        For the file format see
        http://www.esi.umontreal.ca/accelrys/life/insight2000.1/xplor/formats.html

        """
        root, ext = os.path.splitext(filename)
        filename = root + '.xplor'

        NA, NB, NC = grid.grid.shape
        AMIN, AMAX = grid.

        a, b, c = [edge[-1] - edge[0] for edge in grid.edges]
        alpha, beta, gamma =  [90.0, 90.0, 90.0]

        header = [
            '',
            '       1',
            'DX2XPLOR',
            f'{NA:>8g}{AMIN:>8g}{AMAX:>8g}' + \
            f'{NB:>8g}{BMIN:>8g}{BMAX:>8g}' + \
            f'{NC:>8g}{CMIN:>8g}{CMAX:>8g}',
            f'{a:>12.5E}{b:>12.5E}{c:>12.5E}' + \
            f'{alpha:>12.5E}{beta:>12.5E}{gamma:>12.5E}'
            'ZXY',
            '       0'
        ] 

        components = dict(
            positions=OpenDX.gridpositions(1, self.grid.shape, self.origin,
                                           self.delta),
            connections=OpenDX.gridconnections(2, self.grid.shape),
            data=OpenDX.array(3, self.grid, type=type, typequote=typequote),
        )
        dx = OpenDX.field('density', components=components, comments=comments)

        dx.write(filename)

def export2XPLOR(grid, filename):

    outmap = open(filename, 'w')




def _main_(inputfile, outputfile):
    """[summary]

    Parameters
    ----------
    inputfile : [type]
        [description]
    outputfile : [type]
        [description]
    """
    grid = gridData.Grid()
    grid.load(inputfile)

    export2XPLOR(grid, outputfile)

    


