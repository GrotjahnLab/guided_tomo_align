# Generate RELION Euler angles and rotation origins from UCSF Chimera sessions

<strong>Overview:</strong>


<strong>Installation</strong>

The easiest way to manage the libraries needed to run these scripts is to install <a href="https://www.anaconda.com/products/individual">Anaconda</a>, and use it to generate the follwing environments:

<code>pychimera</code>, with the libraries necessary to interpret UCSF Chimera session files.

<code>py37</code>, with a version scipy that has the Rotation object.

1) Install Anaconda following the instruction in their website.

2) Clone this repository:

<code>git clone https://github.com/GrotjahnLab/THISREPO.git</code>
<code>cd THISREPO</code>

3) For the pychimera library to work, you need to install UCSF Chimera and direct pychimera to its directory. See pychimeras' help for more information, specially points 2 and 4 in this <a href="https://pychimera.readthedocs.io/en/latest/install.html">page</a>. Avoiding launching of the UCSF Chimera GUI may be desirable, specially when working from a computing cluster. For this, make sure you obtain the UCSF Chimera "headless" version. In order to execute the downloaded \*.bin file, ma
ke it into an executable by running <code>chmod +x ucsfchimera\_download.bin</code>.

4) Create <code>pychimera</code> and <code>py37</code> using the provided \*.yml files:

<code>conda env create -f ./pychimera.yml</code>
<code>conda env create -f ./py37.yml</code>

5) First, activate the pychimera environment using <code>conda activate pychimera</code> to run <code>chim\_session\_to\_mtx.py</code>. See <code>ribosome\_example.sh</code> for an example.

6) Then, activate the py37 environment using <code>conda activate py37</code> to run <code>mtx\_to\_star.py</code>.

7) There is a known issue with some UCSF Chimera installations where the libgfxinfo.so library will produce a "undefined symbol" error. We have been able to finx this by removing the pcre package from the pychimera environment: <code>conda remove --force pcre</code>
