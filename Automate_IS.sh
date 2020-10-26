#!/bin/bash

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

STACKGANPATH=${1:-/home/monash/Desktop/StackGAN-v2-master/code}
IS_PATH=${2:-/home/monash/Desktop/StackGAN-inception-model-master}

cd $STACKGANPATH



check=`python $SCRIPTPATH/update_pth.py -m init -n netG_200000 -d $STACKGANPATH`
counter=0

while [ "$check" != "None" ] && [ "$counter" -lt 12 ] 
do
	# run program to generate images
	python main.py --cfg cfg/eval_birds.yml --gpu 0

	# compute IS in separate terminal tab and save output into logfile_netG$check.txt (use -hold to keep xterm open)
	# python inception_score.py --image_folder $IMG_PATH
	# & symbol to use multithreading so current (parent) terminal does not wait for IS to finish 
	echo $check
	IMG_PATH="/home/monash/Desktop/StackGAN-v2-master/models/birds_3stages/iteration$check/single_samples/valid"
	xterm -e "
		cd $IS_PATH; 
		python inception_score.py --image_folder $IMG_PATH | tee logs/logfile_netG$check.txt;" &

	# update yml file
	check=`python $SCRIPTPATH/update_pth.py -d $STACKGANPATH`
	counter=$(( counter + 1 ))

done



