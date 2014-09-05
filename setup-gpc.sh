#!/bin/bash

set -e

COMP=$1
NUM=$2
myNEX=$3
SHORT=$4
OLD_AK135=$5
OLD_CONF=$6


if [ "$COMP" == "ifort" ]; then
	# Test with Intel
	module purge
	module load intel/12.1.3 openmpi/1.4.4-intel-v12.1
elif [ "$COMP" == "gfortran" ]; then
	# Test with gfortran
	module purge
	module load gcc/4.6.1 openmpi/1.4.4-gcc-v4.6.1
else
	echo "Unknown compiler!"
	exit 1
fi


mkdir -p $SCRATCH/test_${COMP}${NUM}_${SHORT}
cd $SCRATCH/test_${COMP}${NUM}_${SHORT}
if [ "$OLD_CONF" == "yes" ]; then
	rsync -av \
		--exclude=.git* \
		--exclude=utils --exclude=UTILS \
		--exclude=EXAMPLES --exclude=examples \
		--exclude=doc \
		~/specfem3d_globe/ .
	./configure
else
	~/specfem3d_globe/configure
fi
mkdir -p OUTPUT_FILES
mkdir -p DATABASES_MPI
mkdir -p DATA
sed "s/ak135-test/ak135-test-${COMP}${NUM}-$SHORT/g" $SCRATCH/ak135-bug/run.gpc > run.gpc
cp $SCRATCH/ak135-bug/CMTSOLUTION DATA/
cp $SCRATCH/ak135-bug/STATIONS DATA/
cp $SCRATCH/ak135-bug/Par_file DATA/
sed -i "s/240/${myNEX}/g" DATA/Par_file
if [ "$OLD_AK135" == "yes" ]; then
	sed -i 's/1D_ak135f_no_mud/1D_ak135/g' DATA/Par_file
fi

