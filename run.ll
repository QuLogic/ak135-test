#=======================================================
# @ shell = /usr/bin/ksh
#
#### For 6x6x6 slice simulation ####
# @ total_tasks = 216
# @ node = 4
# @ wall_clock_limit = 04:00:00
#
# @ job_name = ak135-test
# @ notification = complete
# @ notify_user = esalesde@physics.utoronto.ca
# @ output = OUTPUT_FILES/$(jobid).out
# @ error = OUTPUT_FILES/$(jobid).err
#
# Don't change anything below here unless you know exactly
# why you are changing it.
#
# @ job_type        = parallel
# @ class           = verylong
# @ rset = rset_mcm_affinity
# @ mcm_affinity_options = mcm_distribute mcm_mem_req mcm_sni_none
# @ cpus_per_core=2
# @ task_affinity=cpu(1)
# @ environment = COPY_ALL; MEMORY_AFFINITY=MCM; MP_SYNC_QP=YES; \
#                MP_RFIFO_SIZE=16777216; MP_SHM_ATTACH_THRESH=500000; \
#                MP_EUIDEVELOP=min; MP_USE_BULK_XFER=yes; \
#                MP_RDMA_MTU=4K; MP_BULK_MIN_MSG_SIZE=64k; MP_RC_MAX_QP=8192
#
#
### newtork IP or US,HIGH
# @ network.MPI = csss,not_shared,US,HIGH
### submit to queue
# @ queue

export MP_LABELIO=yes
export MP_COREFILE_FORMAT=STDERR
 
export jobid=$LOADL_JOB_NAME

echo "====$LOADL_JOB_NAME ===="
echo "====$LOADL_STEP_ID ===="

./bin/xmeshfem3D
./bin/xspecfem3D

# check if simulation is successful
grep "End of the simulation" OUTPUT_FILES/output_solver.txt
if [ $? != 0 ]; then
    echo "*** The simulation did not end successfully, double check! ***"
fi

find DATABASES_MPI -type f | xargs rm
