#!/bin/bash
#
#    Sync obs data to the work area
#
#     Ver 1.0  2018/11/21   H. Akitaya
#     Ver 1.1  2018/12/05   H. Akitaya; bug fix for no argument


obsdir=/home/Student13/obs
jgemworkdir=/workarea/Student13/jgem
period=20  # sec

usage()
{
    echo "$0 dirname (yyyymmdd)"
}

if [ $# -le 0 ]; then
    usage
    exit
fi

datedir=$1
if [ "${datedir}" == "" ]; then
    usage
    exit
fi

if [ ! -d ${obsdir}/${datedir} ]; then
    echo "${obsdir}/${datedir} not found."
    exit 1
fi

while :
do
    echo "rsync -auv ${obsdir}/${datedir} ${jgemworkdir}/"
    rsync -auv ${obsdir}/${datedir} ${jgemworkdir}/
    echo "sleep ${period} sec. (Ctrl+C for cease)"
    sleep ${period}
done
