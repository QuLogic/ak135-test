#!/bin/bash

set -e

COMP=$1
NUM=$2
SHORT=$3


cd $SCRATCH/test_${COMP}${NUM}_${SHORT}
if [ "$COMP" == "ifort" ]; then
	module purge
	module load intel/12.1.3 openmpi/1.4.4-intel-v12.1
	make mesh spec
	qsub run.gpc
elif [ "$COMP" == "gfortran" ]; then
	module purge
	module load gcc/4.6.1 openmpi/1.4.4-gcc-v4.6.1
	make mesh spec
	qsub run.gpc
elif [ "$COMP" == "xlf" ]; then
	ssh tcs02 ". /etc/bashrc && module load gmake && cd $PWD && make mesh spec && llsubmit run.ll"
elif [ "$COMP" == "xlf_strict" ]; then
	ssh tcs02 ". /etc/bashrc && module load gmake && cd $PWD && make mesh spec && llsubmit run.ll"
else
	echo "Unknown compiler!"
	exit 1
fi

