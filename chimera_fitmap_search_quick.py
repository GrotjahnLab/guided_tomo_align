import os
from chimera import runCommand as rc
from glob import glob
import random
import argparse

argparser = argparse.ArgumentParser(description='This script uses the UCSF Chimera fitmap function to generate sessions \
                                                with a reference density of interest \
                                                docked in a series of subtomograms. \
                                                We recomend to first open a few subtomograms along the reference to evaluate \
                                                ideal isosurface countour levels. See Volume Viewer > Level in the UCSF Chimera \
                                                graphical interface.')
argparser.add_argument('--subtomogram_path',required=True, type=str,help='Absolute path to directory where all subtomograms are stored, e.g., "/User/sessions/*.mrc"')
argparser.add_argument('--reference_path',required=True, type=str,help='Absolute path to reference density. E.g., "./low_passed_ribosome.mrc"')
argparser.add_argument('--s_angpix',required=True, type=float,help='Pixel size of subtomograms')
argparser.add_argument('--r_angpix',required=True, type=float,help='Pixel size of references')
argparser.add_argument('--s_level',required=True, type=float,help='Subtomogram isosurface contour level')
argparser.add_argument('--r_level',required=True, type=float,help='Reference isosurface contour level')
args = argparser.parse_args()


tomos = glob(args.subtomogram_path)
random.shuffle(tomos)
print('All index origins will be set to 0,0,0.')
for tomo in tomos:
	# skip if file already generated
	tomobase = os.path.basename(os.path.splitext(tomo)[0])
	if os.path.isfile(tomobase+".autodocked.py"): continue	
	# if doesn't exist, touch so no other mpi instances process it
	open("%s.autodocked.py"%tomobase,'a').close()
	print tomobase
	rc("open %s"%tomo)
	rc("volume #0 voxelSize %0.3f originIndex 0,0,0 level %0.3f"%(args.s_angpix,args.s_level))
	rc("open %s"%args.reference_path)
	rc("volume #1 voxelSize %0.3f originIndex 0,0,0 level %0.3f"%(args.r_angpix,args.r_level))
	rc("fitmap #1 #0 search 1000 listfits false")
	rc("save %s.autodocked.py"%tomobase)
	rc("close all")
exit()


