# Interpolation-of-.trc-file
Interpolate null values in .trc' mocap files generated from OptiTrackMotive files.

The main function of this code is to intercept the coordinate data behind the table header in the source file, and interpolate the null values in the data. For the null value in each column, inner interpolation is performed when the header data is data, and external interpolation is performed when the null value is at the head or tail of the column.
The method is to intercept the data without the header and generate a new file (without the header data)
'a.trc' and 'b.trc' in the 'HIL' folder are the original data files, and the processed files are stored in the 'generation' folder.

#################
alpha.py handles a single file and handles null values in a single file.
double_process.py processes multiple files and processes two files.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

对OptiTrackMotive文件生成的.trc'动作捕捉文件内的空值进行插值处理。

该代码的主要功能是截取源文件内，表头后面的坐标数据，对数据内的空值进行插值处理。对于每列内的空值在有头数据为数据的情况下进行内侧插值处理，对于空值就处在该列的头或者尾的情况进行外部插值处理。
方法是将除去表头的数据截取出来，生成新的文件（不含表头数据）
'HIL'文件夹内的'a.trc'和'b.trc'为原数据文件，处理后生成的文件存放在'generation'文件夹内。

################
alpha.py是处理单一文件的，对单一文件内的空值进行处理。
double_process.py是处理多个文件的，对两个文件进行处理。
