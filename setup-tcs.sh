#!/bin/bash

set -e

SHORT="$1"
if [ -z "$SHORT" ]; then
	echo "No commit specified!"
	exit
fi
XLF="$2"
if [ -z "$XLF" ]; then
	echo "No compiler type specified!"
	exit
fi
OLD_AK135="$3"

NEX=( [1]=96 [2]=144 [3]=192 [4]=240 )

# Test with xlf
for i in {1..2}; do
	DIR=$SCRATCH/test_${XLF}${i}_${SHORT}
	mkdir -p $DIR
	(
		cd $DIR
		~/specfem3d_globe/configure FC=xlf2003_r MPIFC=mpxlf2003_r CC=xlc_r
	) &
done

wait

for i in {1..2}; do
	DIR=$SCRATCH/test_${XLF}${i}_${SHORT}
	mkdir -p $DIR/OUTPUT_FILES
	mkdir -p $DIR/DATABASES_MPI
	mkdir -p $DIR/DATA
	sed "s/ak135-test/ak135-test-${XLF}${i}-$SHORT/g" $SCRATCH/ak135-bug/run.ll > $DIR/run.ll
	cp $SCRATCH/ak135-bug/CMTSOLUTION $DIR/DATA/
	cp $SCRATCH/ak135-bug/STATIONS $DIR/DATA/
	cp $SCRATCH/ak135-bug/Par_file $DIR/DATA/
	sed "s/240/${NEX[$i]}/g" $DIR/DATA/Par_file > $DIR/Parfile.tmp
	if [ "$OLD_AK135" == "yes" ]; then
		sed 's/1D_ak135f_no_mud/1D_ak135/g' $DIR/Parfile.tmp > $DIR/DATA/Par_file
		rm $DIR/Parfile.tmp
	else
		mv $DIR/Parfile.tmp $DIR/DATA/Par_file
	fi
done

