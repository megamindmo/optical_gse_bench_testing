#!/bin/bash

#run the file by using source setup.sh otherwise this will run in a sub-shell not your currnet.
export PYTHONPATH="$PWD/quad_cell_scripts"
export PYTHONPATH=$PYTHONPATH:/"$PWD/gui_scripts"
export PYTHONPATH=$PYTHONPATH:/"$PWD/camera_scripts"
export PYTHONPATH=$PYTHONPATH:/"$PWD/zaber_mirror"
export PYTHONPATH=$PYTHONPATH:/"$PWD/influxdb_scripts"
export PYTHONPATH=$PYTHONPATH:/"$PWD/testing_scripts"

echo "done"
