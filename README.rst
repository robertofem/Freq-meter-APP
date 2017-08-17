.. role:: bash(code)
   :language: bash

Frequency-meter APP
===================

<<<<<<< HEAD
Application with an integrated User Interface (UI) for communicating with a frequency meter attached to an FPGA and displaying its state

To run the application in Windows:
* Install Python 3 (pip should already come with Python 3 installer, otherwise install it)
* Open command prompt. Navigate till the project folder.
* pip3 install -r requirements.txt
* pip3 install SIP
* Download qt from https://download.qt.io/archive/qt/4.8/4.8.6/ and install it
* Add C:\Qt\4.8.6\bin to the Windows PATH (Right click My Computer->Advanced Configuration->Environment Variables->PATH).
*
=======
:Author:
    Department of Electronic Technology,

    University of Vigo

:Version: 1.0.0-alpha

Application with an integrated Graphical User Interface (GUI) for communicating with a frequency meter attached to an FPGA and displaying its state.

Ubuntu 16.04 set-up for developing
==================================

First of all, download the project source code from the repository with *git*. The project will be stored on a local folder named **Frequency-meter-APP**:

.. code-block:: bash

   cd ~/<path-to-chosen-parent-folder>
   git clone https://github.com/jlrandulfe/Frequency-meter-APP.git

Create a virtual environment and, with the *pip* tool, install the required python packages for the project. Note that the installed python version must be specified on the environment creation (Can be obtained typing :bash:`python3 --version`):

.. code-block:: bash

   # Install pip for installing Python3 packages
   sudo apt-get install python3-pip
   # Install the virtual environment management library; and set-up commands and OS environment
   sudo pip3 install virtualenvwrapper
   export WORKON_HOME=$HOME/.virtualenvs
   source /usr/local/bin/virtualenvwrapper.sh
   # Create a Python3 virtual environment and install the project dependencies
   mkvirtualenv -p python3.X <env-name>
   cd ~/<path-to-chosen-parent-folder>/Frequency-meter-APP
   pip3 install -r requirements.txt

Finally, install a required system library, which can not be installed with *pip*:

.. code-block:: bash

   sudo apt-get install python3-tk

>>>>>>> c56303de31512e7371518091de837a9449ea37f6
