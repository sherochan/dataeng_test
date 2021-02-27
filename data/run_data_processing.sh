#!/bin/sh
CWD="$(pwd)"
echo $CWD
/usr/local/bin/python /data_processing_Q1.py /data/dataset2.csv >> ~/crondata2.log 
/usr/local/bin/python /data_processing_Q1.py /data/dataset1.csv >> ~/crondata1.log 

echo "Completed!"
