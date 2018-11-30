#!/bin/bash
#
#
#  J-GEM Image Preprocess
#
#       Ver 1.0   2018/11/21  H. Akitaya
#

sacrareddir=/home/Student13/sacra_tools/sacrared
bands='r i z'

usage()
{
    echo "$0 objname exptime(s)"
}

if [ $# -lt 2 ]; then
    usage
    exit 1
fi

objname=$1
exptime=$2

echo "Preprocess for $objname $exptime(s) (y/N)"
read preproc
if [ ! "${preproc}" == "y" ];then
    exit 1
fi

for band in ${bands}; do
    echo "${sacrareddir}/musashi_addheader.py *.fits */*.fits"
    ${sacrareddir}/musashi_addheader.py *.fits */*.fits
    echo "${sacrareddir}/preproc.py ${objname} ${band} ${exptime}"
    ${sacrareddir}/preproc.py ${objname} ${band} ${exptime}
done

echo "WCS application for *_fl.fits (y/N)"
read wcsappli
if [ ! "${wcsappli}" == "y" ];then
    exit 1
fi

for band in ${bands}; do
    echo "${sacrareddir}/wcsresolve.sh ${band}*_fl.fits"
    ${sacrareddir}/wcsresolve.sh ${band}*_fl.fits
done



