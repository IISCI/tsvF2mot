#!/usr/bin/env python
# python 2.7
from __future__ import print_function
from numpy import linspace
import c3d
import argparse


"""
MOT File description:

The topics covered in this section include:

Overview
Representing Joint Angles in a .mot File
Representing Ground Reaction Data in a .mot File
NaNs in your force file
Overview
The .mot (motion) file format was created by the developers of SIMM (Software for Interactive Musculoskeletal Modeling). 
The .mot file format is compatible with both SIMM and OpenSim. A .mot file consists of two parts: 
the motion header and the data. The motion header can come in two forms: (1) SIMM header only or (2) OpenSim and SIMM header.

Form (1) of a motion header looks like this:

subject01_walk1_grf.mot
version=1
datacolumns 19
datarows 9009
range 0.000000 15.013300
endheader
The first line must start with name followed by a space and the name of the .mot file.
The next line should contain datacolumns, a space, and then the total number of columns of data in the .mot file (including the time column). 
The next line should contain datarows, a space, and then the total number of rows of data in the .mot file. 
A later line should contain range, a space, the first time value in the time column, a space, 
and then the last time value in the time column. Optionally, other comments could be included in subsequent lines. 
The final line endheader indicates the end of the header.

Form (2) of a motion header looks like this:

Coordinates
nRows=500
nColumns=24
 
Units are S.I. units (second, meters, Newtons, ...)
Angles are in degrees.
  
endheader

The first line is the name, which is Coordinates in this case, to be used to represent this .mot file when it is loaded into OpenSim. 
This does not have to be the name of the .mot file. 
The second line contains nRows= followed by the number of rows of data in the .mot file. 
The third line contains nColumns= followed by the number of columns of data (including the time column) in the .mot file. 
The fourth line is empty. 

Note that extra lines containing newline characters or comments can be included before the endheader line in the 
SIMM header section of both forms (1) and (2) of the .mot motion header.

Immediately after the endheader line, the data section of the .mot file begins.
The first line after the endheader line should contain tab-delimited labels for each column of (tab-delimited) data in the .mot file.
The first column is usually time, followed by values that vary with time such as generalized coordinates, marker coordinates, ground reaction forces and moments, 
centers of pressure, muscle activations, or muscle lengths.

In old SIMM .mot files, there is no time column, in which case OpenSim uses the range specified in the SIMM header and assumes a fixed time step to specify the time interval 
for the motion. The names of the column labels should match the names used in the model with which the .mot file is intended 
to be used. The rows below this line of column labels must be the corresponding values of each of these quantities at the time 
represented by the first number in each row.

The time values in the time column of a .mot file must be uniformly spaced. An example .mot file (subject01_walk1_grf.mot) 
is provided in the examples/Gait2354_Simbody directory, which is part of the OpenSim distribution.

Representing Joint Angles in a .mot File
Optionally, if joint angles have been computed previously using other software, they may be imported into OpenSim in addition 
to marker data. The joint angles must be provided in a .sto or .mot file. The .mot file must contain a header. Below the header, 
there must be a row of column labels, and the corresponding columns of data below that. Time must be the first column and the 
generalized coordinates of the model must be the subsequent columns. Angles in .mot files are assumed to be in degrees.

Representing Ground Reaction Data in a .mot File
You need to represent your ground reaction data in a .mot file for input into OpenSim. An example file (subject01_walk1_grf.mot) 
is given in the examples/Gait2354_Simbody directory, which is part of the OpenSim distribution.

The first row below the header in the .mot file may contain the following column headings.
As of OpenSim version 2.3.2 the column headers need to be unique
(the program will ask you to save the file in this format first if using a file that doesn't conform to this format).

Also each group of three force, point or torque columns should have a common prefix.: 

time, ground_force_vx, ground_force_vy, ground_force_vz, ground_force_px, ground_force_py, ground_force_pz,

l_ground_force_vx, l_ground_force_vy, l_ground_force_vz, l_ground_force_px, l_ground_force_py, l_ground_force_pz,

ground_torque_x, ground_torque_y, ground_torque_z,

l_ground_torque_x, l_ground_torque_y, l_ground_torque_z

All rows below this line contain the corresponding data in each column.

Columns 2-4 (ground_force_vx, ground_force_vy, ground_force_vz) 
represent the x, y, and z components of the right foot's ground reaction force vector 
in a specific body coordinate system (ground for the model coordinate system). 

Columns 5-7 represent the x, y, and z components of the right foot's center of pressure 
(i.e., the point at which the ground reaction force is applied to the right foot). 

Similarly, columns 8-13 represent the ground reaction force vector and center of pressure for the left foot. 

Columns 14-16 represent the x, y, and z components of the right foot's ground reaction moment vector 
(typically in the model coordinate system). The last three columns represent the analogous quantities for the left foot.

NaNs in your force file
NaNs are not compatible with any dynamics analysis and must be removed from mot files. Force data is splined during computation 
and occurrences of NaNs cause the entire force, moment, or COP column to become NaN.  NaNs often occur when computing COP; 
more details can be found in the C3D files documentation. 

Importing Force Data:  COP and NaNs in c3d files - additional notice
When you import your force data, you can use the origin of the force plate or center of pressure (COP) to express the forces. 
The C3DFileAdapter includes an input parameter (ForceLocation) that allows you to choose OriginOfForcePlate or CenterOfPressure. 
Using the COP is helpful for visualization, but can lead to NaN values. In particular, when the force values go to zero, 
the COP value is undefined (NaN). This is problematic during Inverse Dynamics analysis as you will get all NaN values for the output 
moments. This is because OpenSim splines the force and COP data before computing joint moments and the splines are undefined 
in the presence of NaNs for your input data. If you find that your mot files are containing NaNs for COPs after conversion, 
you can use the OriginOfForcePlate flag when you import your C3D data. 

________________________________________________________________________________________________________


STO File description:
Storage (.sto) Files
The .sto file format was created by the developers of OpenSim. It is very similar to the .mot file format, with two main differences:

The time values in the time column of a .sto file do not have to be uniformly spaced
The first column of a .sto file must contain time, whereas a .mot file can contain other quantities in the first column
There is only one format for the header of a .sto file and it is very simple, as shown below:

Coordinates
nRows=153
nColumns=24
endheader
The first line contains the name with which the .sto file will be referred to when it is loaded into OpenSim. 
The second line is nRows= followed by the number of rows of data in the .sto file. 
The third line is nColumns= followed by the number of columns of data in the .sto file (including the time column). 
The last line is endheader. Immediately following the endheader line is the data section of the .sto file, 
which is identical to the data section of a .mot file, except that the time column is allowed to have non-uniform spacing.

Example .sto files, such as subject01_walk1_RRA_Actuation_force.sto, are provided 
in the examples/Gait2354_Simbody/OutputReference/ResultsRRA directory, which is part of the OpenSim distribution. 
As of version 2.3.2, the sto files have a header that includes:

Version number (version=1)
Whether angular data specified in the file are in radians or degrees (inDegrees=yes/no). 
OpenSim would assume that old sto files are in radians, if this is not the case you can manually change this flag in the file 
or use the Help->Convert Files option to set it.


This program converts a TSV file to STO or MOT (text) format.


todo:

- Split file data on two legs - left and right by its middle frame - DONE!
- Add left and right leg forces data fields - DONE!
- Fill empty leg with previous data from this leg - Filled with zeros (check results!)

- Convert time column to uniformly spaced values for .mot file case - but it seems that that doesn't affect OSIM file feeding results - DONE!
- rotate axis: .trc marker data converted using rotations = [90, 180, 0]
		    	X_opensim = -X_QTM
		    	Y_opensim = Z_QTM
		    	Z_opensim = Y_QTM
"""

parser = argparse.ArgumentParser(
    description='Convert a TSV file to STO (text) format.')
parser.add_argument('input', default='-', metavar='FILE',
                    nargs='+', help='process data from this input FILE')

def pad(str_float_value):
    """
    Pad value with zeroes to 8 digits after dot
    """
    return "%.8f"%float(str_float_value)

def reverse_axis(x_data):
    """
    Reverse axis
    Axis = -Axis
    """
    if x_data[:1] == '-':
        x_data = x_data[1:]
    else:
        x_data = '-'+x_data
    return x_data

def scale_axis(axis_data, factor):
    """
    Scale axis data by factor
    X (string) = factor * X 

    Arguments:
    axis_data = axis to scale
    factor = scale factor (float)
    """
    scaled_axis = str(float(axis_data)*factor)
    return scaled_axis

def shift_axis(axis_data,shift_ammount):
    """
    Shift Axis origin

    Arguments:
    axis_data = axis to shift
    shift_amount = amount for shift
    """
    shifted_axis = pad(str(float(axis_data)+shift_ammount))
    return shifted_axis

def convert(filename):
    if filename != '-':
        # input = open(filename, 'r')
        # output = open(filename.replace('.tsv', '.sto'), 'w')
        pass
    # Read TSV file and store in line_data list
    line_data = []
    with open(filename, 'r') as f:
        for line in f:
            # read data rows from file and pack it into line_data list object
            line_data.append(line)

    with open(filename.replace('.tsv', '.mot'), 'w') as f:
        f.write(filename.replace('.tsv', '.mot')+'\n')
        print (filename.replace('.tsv', '.mot'))
        f.write('version=1'+'\n')
        print ('version=1')
        # code to calculate Rows and Columns count of data field
        header_rows = 0  # Start number of rows
        time = 0.0  # Start time
        # quant = []  # array of uniformly spaced time values in case of wikipedia definition 0..1
        quant = 0  # Start frame size in milliseconds
        data_flag = False # Marker of header end
        frame_number = 0 # Start frame number
        zero_tuple = '0.00000000', '0.00000000', '0.00000000'  # zero values for flying leg

        #lambda for space padding goes here

        for i in line_data:
            header_rows += 1

            if i[:9] == 'FREQUENCY':
                # get frequency from FREQUENCY data field in TSV file
                frequency = int(i.split()[1])
                quant = 1.0 / frequency  # Calculate frame size in milliseconds 
                # recalculated later by uniformly spaced values method for time column if we use wikipedia definition 0..1
           
            if i[:7] == 'Force_X':
                # Count columns in data part plus 1 time column
                # Added right number of columns with left leg and time data
                n_columns = len(i.split())+1+9
                n_columns_str = 'nColumns='+str(n_columns)+'\n'
                total_rows = sum(1 for line in open(filename))
                n_rows = total_rows - header_rows
                n_rows_str = 'nRows='+str(n_rows)+'\n'
                
                dataset_half = n_rows/2  # counter for half of frames count to split legs force data

                # make time column uniformly spaced 0..1 quant now array of such values
                # quant = linspace(0, 1, n_rows) - wrongly defined and means just splitting by the same values

                f.write(n_rows_str)
                print(n_rows_str)
                f.write(n_columns_str)
                print(n_columns_str)
                mot_column_header = "\t".join("   R_ground_force_vx,    R_ground_force_vy,    R_ground_force_vz,    R_ground_force_px,    R_ground_force_py,    R_ground_force_pz,    L_ground_force_vx,    L_ground_force_vy,    L_ground_force_vz,    L_ground_force_px,    L_ground_force_py,    L_ground_force_pz,    R_ground_torque_x,    R_ground_torque_y,    R_ground_torque_z,    L_ground_torque_x,    L_ground_torque_y,    L_ground_torque_z".split(', '))
                # new header according to .mot documentation and add time column in the begining of data part of file
                i = 'time\t'.rjust(21)+mot_column_header+'\n'
                f.write('inDegrees=yes'+'\n')
                # this indicates, that all values are in degrees for angles, bot it is optional for forces only data files
                print('inDegrees=yes')
                f.write('endheader'+'\n')
                print('endheader')  # header end sign
                f.write(i)
                print (i) # Debug header titles
                data_flag = True
                continue
            if not data_flag:  # Check if it is still header then write additional data from .tsv
                # f.write(i) # skip additional fields to be written from .tsv file, uncomment it if you want to write this data to .mot file, but check position in file!
                # just output this additional data to console
                print ('EXTRA FIELD - NOT WRITTEN TO .mot FILE:', i)
            else:  # Header ended - add time data column to the each row of data

                # Get Force_X|Force_Y|Force_Z|Moment_X|Moment_Y|Moment_Z|COP_X|COP_Y|COP_Z from .tsv file - right foot first half of file cut
                data_string_split = i.split()

                # print (data_string_split) # debug output of .tsv data fields order.

                data_string_split[0] = pad(data_string_split[0]) # Force Vx
                data_string_split[3] = pad(data_string_split[3]) # Moment Mx
                data_string_split[6] = pad(scale_axis(data_string_split[6], 0.001)) # COP Px with no reverse scaled

                # Swap Y and Z for force, moment and cop for QTM 2 OSIM Axis rotations

                data_string_split[1], data_string_split[2] = pad(data_string_split[2]), pad(data_string_split[1]) # Force Y,Z to Z,Y
                data_string_split[4], data_string_split[5] = pad(data_string_split[5]), pad(data_string_split[4]) # Moment Y,Z to Z,Y
                data_string_split[7], data_string_split[8] = '0.00000000', pad(scale_axis(reverse_axis(data_string_split[7]), 0.001)) # 0.000000 for COP Y and reverse scaled COP Z
                # cop Y,Z to Z,Y
                
                data_string_split[2], data_string_split[0] = data_string_split[2], data_string_split[0] # Vz - Vz
                data_string_split[5], data_string_split[3] = data_string_split[3], data_string_split[5] # Mz - Mz
                data_string_split[8], data_string_split[6] = data_string_split[6], data_string_split[8] # Px - Pz

                # Reverse Axis

                #data_string_split[0] = reverse_axis(data_string_split[0]) # reverse Vx
                data_string_split[3] = reverse_axis(data_string_split[3]) # reverse Mx
                data_string_split[6] = reverse_axis(data_string_split[6]) # reverse Px

                data_string_split[2] = reverse_axis(data_string_split[2]) # reverse Vz
                data_string_split[5] = reverse_axis(data_string_split[5]) # reverse Mz
                data_string_split[8] = reverse_axis(data_string_split[8]) # reverse Pz
                
                # Shift Axis

                data_string_split[0] = shift_axis(data_string_split[0],-0.5) # shift Vx
                data_string_split[3] = shift_axis(data_string_split[3],-0.5) # shift Mx
                data_string_split[6] = shift_axis(data_string_split[6],-0.5) # shift Px
                
                data_string_split[2] = shift_axis(data_string_split[2],0.25) # shift Vz
                data_string_split[5] = shift_axis(data_string_split[5],0.25) # shift Mz
                data_string_split[8] = shift_axis(data_string_split[8],0.25) # shift Pz
                
                """# swap moment(torque) and cop(p) from .tsv order to .mot order of columns
                    
                # Moment(torque) - we have to calculate it later according to https://www.c-motion.com/v3dwiki/index.php?title=FP_Type_6
                # swap_tuple_m = data_string_split[3], data_string_split[4], data_string_split[5]
                # We have to calculate Tz moment as defined above

                # cop
                swap_tuple_p = data_string_split[6], data_string_split[7], data_string_split[8]

                # cop
                data_string_split[3], data_string_split[4], data_string_split[5] = swap_tuple_p

                # cop zero debug
                # data_string_split[4] = '0'

                # left leg force = 0
                data_string_split[6], data_string_split[7], data_string_split[8] = zero_tuple

                data_string_split.extend(zero_tuple)  # left leg cop = 0

                #data_string_split.extend(swap_tuple_m)  # moment(torque) # we will calculate Tz rotation moment later
                data_string_split.extend(zero_tuple)  # moment(torque) = 0 - 0 - 0 padding with zeros for now
                # left leg moment(torque) = 0
                data_string_split.extend(zero_tuple)
                """

                if frame_number < dataset_half:  # RIGHT LEG DATA

                    # swap moment(torque) and cop(p) from .tsv order to .mot order of columns
                    
                    # moment(torque) - we have to calculate it later according to https://www.c-motion.com/v3dwiki/index.php?title=FP_Type_6
                    # swap_tuple_m = data_string_split[3], data_string_split[4], data_string_split[5]
                    # We have to calculate Tz moment as defined above

                    # cop
                    swap_tuple_p = data_string_split[6], data_string_split[7], data_string_split[8]

                    # cop
                    data_string_split[3], data_string_split[4], data_string_split[5] = swap_tuple_p

                    # cop zero debug
                    # data_string_split[4] = '0'

                    # left leg force = 0
                    data_string_split[6], data_string_split[7], data_string_split[8] = zero_tuple

                    data_string_split.extend(zero_tuple)  # left leg cop = 0

                    #data_string_split.extend(swap_tuple_m)  # moment(torque) # we will calculate Tz rotation moment later
                    data_string_split.extend(zero_tuple)  # moment(torque) = 0 - 0 - 0 padding with zeros for now
                    # left leg moment(torque) = 0
                    data_string_split.extend(zero_tuple)

                else:  # LEFT LEG DATA

                    # print (data_string_split) # debug output of .tsv data fields order.

                    swap_tuple_f = data_string_split[0], data_string_split[1], data_string_split[2]
                    # swap_tuple_m = data_string_split[3], data_string_split[4], data_string_split[5] # unused since we have to calculate Tz moment later
                    swap_tuple_cop = data_string_split[6], data_string_split[7], data_string_split[8]

                    # right foot force - zero
                    data_string_split[0], data_string_split[1], data_string_split[2] = zero_tuple
                    # right foot cop - zero
                    data_string_split[3], data_string_split[4], data_string_split[5] = zero_tuple

                    # left foot force
                    data_string_split[6], data_string_split[7], data_string_split[8] = swap_tuple_f

                    data_string_split.extend(swap_tuple_cop)  # left foot cop

                    # right foot moment - zero
                    data_string_split.extend(zero_tuple)

                    # data_string_split.extend(swap_tuple_m)  # left foot moment # we will calculate Tz rotation moment later
                    data_string_split.extend(zero_tuple) # moment(torque) = 0 - 0 - 0 padding with zeros for now

                # create tab separated and space padded row of GRF values space padded for better look in text viewers
                splt = ''
                result = ''
                final_result = ''
                for i in data_string_split:
                    # print (i)
                    splt = i.split('.')
                    for x in splt:
                        if x[:1] == '-':
                            x = x[0:]
                            if len(result) <1:
                                result = result+x.rjust(11)
                            else:
                                result = '-'+result+'.'+x
                        elif len(result) <1:
                            result = result+x.rjust(11)
                        else:
                            result = result+'.'+x
                    
                    final_result = final_result+result+'\t'
                    
                    result = ''
                    

                #i = ''.rjust(10)+'\t'.ljust(11).join(data_string_split) # add sapaces in front and behind values for better view in text format
                i = final_result.rstrip('\t')

                # print (i) # debug
                data_row_str = pad(str(time)).rjust(20)+'\t'+i+'\n'
                f.write(data_row_str)
                # print (data_row_str) # Debug output disable

                frame_number += 1
                time = time + quant # adds unform space calculated in quant variable

                """
                # pick uniformly spaced value from precalculated array of such values for given frame number
                # next frame
                if frame_number == n_rows: # check if it is a last frame to prevent index out of range in unformly spaced values array quant[]
                    break
                else:
                    time = quant[frame_number]
                """

        print (filename.replace('.tsv', '.mot'),' Done!')


def main(args):
    for filename in args.input:
        convert(filename)


if __name__ == '__main__':
    main(parser.parse_args())
