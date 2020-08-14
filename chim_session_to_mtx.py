#!/nfs/home/bbasanta/anaconda2/envs/pychimera/bin/python

from glob import glob
import numpy as np
import json
import argparse
import sys

def process_session_string_sk(fname,refname):
    '''
    Returns the rotation axis and angle of the reference.
    '''
    f = open(fname,'r')
    lines = [i[:-1] for i in f.readlines()]
    rot_angle = None
    rotation_axis = None
    translation = None
    line_found = False
    idx_found = 0
    for n,line in enumerate(lines):
        if line.startswith('          \'name\': u\'%s\''%refname): line_found = True
        if line_found:
            idx_found += 1
            if idx_found == 10:
                rot_angle = float(line.split()[-1][:-1])
            if idx_found == 11:
                rotation_axis = [float(line.split()[2][:-1]), float(line.split()[3][:-1]), float(line.split()[4][:-1])]
            if idx_found == 12:
                translation = [float(line.split()[2][:-1]), float(line.split()[3][:-1]), float(line.split()[4][:-1])]
                break
    if not line_found: print('WARNING! no reference found in session %s'%fname); raise ValueError
    return (rot_angle,rotation_axis,translation)

def process_session_string_tm(fname,part_prefix,part_postfix):
    '''
    Returns the rotation axis and angle of the particle.
    '''
    #print('Searching for pattern %s and %s'%('          \'name\': u\'%s'%part_prefix, '%s\','%part_postfix))
    f = open(fname,'r')
    lines = [i[:-1] for i in f.readlines()]
    rot_angle = None
    rotation_axis = None
    translation = None
    line_found = False
    idx_found = 0
    part_name = ''
    for n,line in enumerate(lines):
        if line.startswith('          \'name\': u\'%s'%part_prefix) and line.endswith('%s\','%part_postfix):
            line_found = True
            part_name = line.split('\'')[-2]
        if line_found:
            idx_found += 1
            if idx_found == 10:
                rot_angle = float(line.split()[-1][:-1])
            if idx_found == 11:
                rotation_axis = [float(line.split()[2][:-1]), float(line.split()[3][:-1]), float(line.split()[4][:-1])]
            if idx_found == 12:
                translation = [float(line.split()[2][:-1]), float(line.split()[3][:-1]), float(line.split()[4][:-1])]    
                break
    if not line_found: print('WARNING! no particle found in session %s'%fname); raise ValueError
    return (rot_angle,rotation_axis,translation,part_name)

def get_matrix(ang,vec,trans):
    '''
    Take the Chimera values and turn them into a transformation matrix in 3D (4x4).
    '''
    xf = chimera.Xform()
    ax = chimera.Vector(vec[0], vec[1], vec[2])
    tr = chimera.Vector(trans[0], trans[1], trans[2])
    xf.translate(tr)
    xf.rotate(ax,ang)
    
    return np.reshape(np.array(xf.getOpenGLMatrix()),(4,4),order='F')

def get_translation(mats,matt,r_angpix,p_angpix,r_ori,p_ori,r_box,p_box):
    # get skeleton origin:
    s_angpix = r_angpix
    s_idx_ori = np.array([(s-1)/2.0 for s in r_box]) - r_ori
    s_ang_ori = np.array([i*s_angpix for i in s_idx_ori])
    s_ang_ori = np.append(s_ang_ori,[1])
    # get tomo origin:
    t_angpix = p_angpix
    t_idx_ori = np.array([(s-1)/2.0 for s in p_box]) - p_ori
    #t_idx_ori = [0,0,0]
    
    t_ang_ori = np.array([i*t_angpix for i in t_idx_ori])
    t_ang_ori = np.append(t_ang_ori,[1])
    # transform origins:
    gc_s = np.dot(mats, s_ang_ori)
    gc_t = np.dot(matt, t_ang_ori)
    # Translation from tomo to skeleton:
    t = gc_s-gc_t
    # Retrotransform to tomo origin:
    final_t = np.dot(np.transpose(matt[:3,:3]), t[:3])
    return (final_t/t_angpix)



if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description='Use UCSF Chimera *.py sessions to extract the rotation \
                                                     matrix that transforms particles to references. \
                                                     It is recommended particle densities are named as they appear in the RELION *.star file.\
                                                     Access to the session MRC files is not required.')
    argparser.add_argument('--sessions_path',required=True, type=str,help='Absolute path to directory where all sessions are stored, e.g., "/User/sessions/"')
    argparser.add_argument('--reference_name',required=True, type=str,help='Name of reference density in the Chimera sessions as it appears in it. E.g., "low_passed_ribosome.mrc"')
    argparser.add_argument('--particle_name_prefix',type=str,help='Prefix used to parse particle densities from Chimera sessions. If all your particles are named "tomogram_<something>.mrc", then use "tomogram_" as prefix to find them in each session.')
    argparser.add_argument('--particle_name_postfix',type=str,help='Postfix used to parse particle densities from Chimera sessions. If all your particles are named "tomogram_<something>_foo.mrc", then use "_foo.mrc" as postfix to find them in each session.')
    argparser.add_argument('--particle_origin',type=str,default='0,0,0',help='Index origin of particle *.mrc if different from 0,0,0. It is assumed to be the same for all particles. Enter as X,Y,Z')
    argparser.add_argument('--reference_origin',type=str,default='0,0,0',help='Index origin of reference *.mrc if different from 0,0,0. Enter as X,Y,Z')
    argparser.add_argument('--particle_angpix',required=True,type=str,help='Pixel size, in Angstroms, of particle *.mrc. It is assumed to be the same for all particles.')
    argparser.add_argument('--reference_angpix',required=True,type=str,help='Pixel size, in Angstroms, of reference *.mrc.')
    argparser.add_argument('--r_box',required=True,type=str,help='Reference box size')
    argparser.add_argument('--p_box',required=True,type=str,help='Particle box size')
    argparser.add_argument('--output_name',default='./matrix_dictionary.txt',type=str,help='Name for output file containing a transformation matrix for each particle.')
    args = argparser.parse_args()

    #import pychimera.__main__
    #update_dict = pychimera.__main__.run()
    import pychimera
    pychimera.patch_environ(nogui=True)
    pychimera.enable_chimera()
    import chimera

    if (not args.particle_name_prefix) and (not args.particle_name_postfix):
        sys.exit('You must provide a particle prefix or postfix')
    sess =  args.sessions_path
    part_prefix = ''
    if args.particle_name_prefix: part_prefix = args.particle_name_prefix
    part_postfix = ''
    if args.particle_name_postfix: part_postfix = args.particle_name_postfix
    print('Will search for particles starting with %s and ending with %s'%(part_prefix,part_postfix))

    refname = args.reference_name
    p_angpix = float(args.particle_angpix)
    r_angpix = float(args.reference_angpix)
    p_ori = np.array( [ float(i) for i in args.particle_origin.split(',') ] )
    r_ori = np.array( [ float(i) for i in args.reference_origin.split(',') ] )
    r_box = [ float(i) for i in args.r_box.split(',') ]
    p_box = [ float(i) for i in args.p_box.split(',') ]
    outf = args.output_name

    sessions = [ i for i in glob(sess+'*.py')]
    print('Found %d sessions'%(len(sessions)))
    out = open(outf,'w')
    for chim_se in sessions:
        try: angs,vecs,trans = process_session_string_sk(chim_se,refname)
        except ValueError: continue
        try: angt,vect,trant,part_name = process_session_string_tm(chim_se,part_prefix,part_postfix)
        except ValueError: continue
        print('Found particle %s'%part_name)
        # These are the transformation matrices extracted from the Chimera session, note they are 3x4:
        mats = get_matrix(angs,vecs,trans)
        matt = get_matrix(angt,vect,trant)
        # Up to here OK!
        # This is the rotation that takes the particle from current state to aligned with oriented reference:
        nu_mat = np.dot(np.transpose(mats[:3,:3]),matt[:3,:3])
        # This is the translation to shift particle box so that the origin of rotation is on the particle density:
        translation = -1*np.array([get_translation(mats,matt,r_angpix,p_angpix,r_ori,p_ori,r_box,p_box)])
        #print(translation)
        #print(p_box)
        if np.array([ abs(t)>dim for t,dim in zip(translation,p_box) ]).any():
            print('WARNING! reference in session %s seems to be outside of the particle box. It will not be saved!'%chim_se)
            continue
        nu_mat = np.append(nu_mat,np.transpose(translation),1) 
        mat = [list(j) for j in nu_mat]
        out.write(json.dumps({part_name:mat})+'\n')
    out.close()



