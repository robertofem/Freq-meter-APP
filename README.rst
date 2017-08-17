.. role:: bash(code)
   :language: bash

Frequency-meter APP
===================

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

Create a virtual environment and, with the *pip* tool, install the required python packages for the project. Note that the installed python version must be specified on the environment creation (Can be obtained typing :bash:`python3 --version`)

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

Finally, install the required system libraries, which can not be installed with *pip*:

.. code-block:: bash

   sudo apt-get install python3-pyqt5
   sudo apt-get install pyqt5-dev-tools
   
