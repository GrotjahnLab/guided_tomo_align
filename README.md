# Generate RELION Euler angles and rotation origins from UCSF Chimera sessions

<strong>Overview:</strong>



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

5) First, activate the pychimera environment using <code>conda activate pychimera</code> to run <code>chim\_session\_to\_mtx.py</code>. Here's an example:

<code>python ./chim\_session\_to\_mtx.py --sessions_path /path/to/chimerasessions/ --reference_name reference.mrc --particle_name_prefix deconv_lam2_TS4 --particle_angpix 10.88 --reference_angpix 10.88 --r_box 44,44,44 --p_box 44,44,44</code>

<code></code>

6) Then, activate the py37 environment using <code>conda activate py37</code> to run <code>mtx\_to\_star.py</code>.

7) There is a known issue with some UCSF Chimera installations where the libgfxinfo.so library will produce a "undefined symbol" error. We have been able to fix this by removing the pcre package from the pychimera environment: <code>conda remove --force pcre</code>
