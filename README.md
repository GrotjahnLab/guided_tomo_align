# Generate RELION Euler angles and rotation origins from UCSF Chimera sessions

<strong>Overview</strong>

Automatic subtomogram aligment for particle reconstruction not always produces the desired outcome. In order to guide particle reconstruction, the use of a reference may be necessary. By manually superimposing a reference density on the desired location of a subtomogram one can guide alignment, this can be done in visualization software, such as UCSF Chimera. We provide two python scripts that together take the reference alignment information from a UCSF Chimera session and produce a RELION \*.star file with initialized Euler angles and rotations origins that transform particles to the reference. This results in the alignment and superimposition of all user-defined subtomogram locations.

<strong>Installation</strong>

The easiest way to manage the libraries needed to run these scripts is to install <a href="https://www.anaconda.com/products/individual">Anaconda</a>, and use it to generate the follwing environments:

<code>pychimera</code>, with the libraries necessary to interpret UCSF Chimera session files.

<code>py37</code>, with a version scipy that has the Rotation object.

1) Install Anaconda following the instruction in their website.

2) Clone this repository:

<code>git clone https://github.com/GrotjahnLab/guided_tomo_align.git</code>

<code>cd guided_tomo_align</code>

3) For the pychimera library to work, you need to install UCSF Chimera and direct pychimera to its directory. See pychimeras' help for more information, specially points 2 and 4 in this <a href="https://pychimera.readthedocs.io/en/latest/install.html">page</a>. Avoiding launching of the UCSF Chimera GUI may be desirable, specially when working from a computing cluster. For this, make sure you obtain the UCSF Chimera "headless" version. In order to execute the downloaded \*.bin file, make it into an executable by running <code>chmod +x ucsfchimera\_download.bin</code>. Finally, set the CHIMERADIR environment variable (in bash): <code>export CHIMERADIR=/your/chimera/intallation/dir/</code>

4) Create <code>pychimera</code> and <code>py37</code> using the provided \*.yml files:

<code>conda env create -f ./pychimera.yml</code>

<code>conda env create -f ./py37.yml</code>

5) First, activate the pychimera environment using <code>conda activate pychimera</code> to run <code>chim\_session\_to\_mtx.py</code>. You can print a help message typing:

<code>python ./chim\_session\_to\_mtx.py --help</code>

It will generate the following output:

    usage: chim_session_to_mtx.py [-h] --sessions_path SESSIONS_PATH
                              --reference_name REFERENCE_NAME
                              [--particle_name_prefix PARTICLE_NAME_PREFIX]
                              [--particle_name_postfix PARTICLE_NAME_POSTFIX]
                              [--particle_origin PARTICLE_ORIGIN]
                              [--reference_origin REFERENCE_ORIGIN]
                              --particle_angpix PARTICLE_ANGPIX
                              --reference_angpix REFERENCE_ANGPIX --r_box
                              R_BOX --p_box P_BOX [--output_name OUTPUT_NAME]

    Use UCSF Chimera *.py sessions to extract the rotation matrix that transforms
    particles to references. It is recommended particle densities are named as
    they appear in the RELION *.star file. Access to the session MRC files is not
    required.

    optional arguments:
       -h, --help            show this help message and exit
       --sessions_path SESSIONS_PATH
                        Absolute path to directory where all sessions are
                        stored, e.g., "/User/sessions/"
       --reference_name REFERENCE_NAME
                        Name of reference density in the Chimera sessions as
                        it appears in it. E.g., "low_passed_ribosome.mrc"
       --particle_name_prefix PARTICLE_NAME_PREFIX
                        Prefix used to parse particle densities from Chimera
                        sessions. If all your particles are named
                        "tomogram_<something>.mrc", then use "tomogram_" as
                        prefix to find them in each session.
       --particle_name_postfix PARTICLE_NAME_POSTFIX
                        Postfix used to parse particle densities from Chimera
                        sessions. If all your particles are named
                        "tomogram_<something>_foo.mrc", then use "_foo.mrc" as
                        postfix to find them in each session.
       --particle_origin PARTICLE_ORIGIN
                        Index origin of particle *.mrc if different from
                        0,0,0. It is assumed to be the same for all particles.
                        Enter as X,Y,Z
       --reference_origin REFERENCE_ORIGIN
                        Index origin of reference *.mrc if different from
                        0,0,0. Enter as X,Y,Z
       --particle_angpix PARTICLE_ANGPIX
                        Pixel size, in Angstroms, of particle *.mrc. It is
                        assumed to be the same for all particles.
       --reference_angpix REFERENCE_ANGPIX
                        Pixel size, in Angstroms, of reference *.mrc.
       --r_box R_BOX         Reference box size
       --p_box P_BOX         Particle box size
       --output_name OUTPUT_NAME
                        Name for output file containing a transformation
                        matrix for each particle.

Here's a commandline example:

<code>python ./chim\_session\_to\_mtx.py --sessions_path /path/to/chimerasessions/ --reference_name reference.mrc --particle_name_prefix deconv_lam2_TS4 --particle_angpix 10.88 --reference_angpix 10.88 --r_box 44,44,44 --p_box 44,44,44</code>

6) Deactivate the <code>pychimera</code> environment by typing <code>conda deactivate</code>. Then, activate the py37 environment using <code>conda activate py37</code> to run <code>mtx\_to\_star.py</code>.

<code>python ./mtx\_to\_star.py --help</code>

It will generate the following output:

       usage: mtx_to_star.py [-h] --template_star TEMPLATE_STAR --chimera_mtx_output
                      CHIMERA_MTX_OUTPUT
                      [--rln_particle_particle_csv RLN_PARTICLE_PARTICLE_CSV]
                      [--angpix ANGPIX] [--output_name OUTPUT_NAME]

       Use transformation matrices generated by chim_session_to_mtx.py to populate a
       template relion star file Euler angles and rotation origins.

       optional arguments:
         -h, --help            show this help message and exit
         --template_star TEMPLATE_STAR
                        RELION *.star file to use as template.
         --chimera_mtx_output CHIMERA_MTX_OUTPUT
                        Output file from chim_session_to_mtx.py
         --rln_particle_particle_csv RLN_PARTICLE_PARTICLE_CSV
                        A "coma separated values" file denoting equivalences
                        between the naming of particles in the *.star file and
                        chimera sessions. E.g., if a particle is named "Partic
                        les/Tomograms/tomogram101/tomogram101_subtomo000004.mr
                        c" in the star file, and "tomo1_4.mrc" in the Chimersa
                        session, the *.csv file should have a line with the
                        following format:
                        "tomogram101_subtomo000004.mrc,tomo1_4.mrc". There
                        should be one pair per line.
         --angpix ANGPIX       Particle pixel size.
         --output_name OUTPUT_NAME
                        Name for output *.star file

Here's a commandline example:

<code>./mtx_to_star.py --template_star you_template.star --chimera_mtx_output matrix_dictionary.txt --rln_particle_particle_csv equiv.csv --angpix 10.88</code>

7) There is a known issue with some UCSF Chimera installations where the libgfxinfo.so library will produce a "undefined symbol" error. We have been able to fix this by removing the pcre package from the pychimera environment: <code>conda remove --force pcre</code>
