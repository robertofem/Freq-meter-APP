.. role:: bash(code)
   :language: bash

Frequency-meter APP
===================

:Author:
    Department of Electronic Technology,

    University of Vigo

:Version: 1.0.0-alpha

Application with an integrated Graphical User Interface (GUI) for communicating with a frequency meter attached to an FPGA and displaying its state.

GNU/Linux set-up for developing
===============================

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
   export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
   source /usr/local/bin/virtualenvwrapper.sh
   # Create a Python3 virtual environment and install the project dependencies
   mkvirtualenv -p python3.X <env-name>
   cd ~/<path-to-chosen-parent-folder>/Frequency-meter-APP
   pip3 install -r requirements.txt

Finally, install a required system library, which can not be installed with *pip*:

.. code-block:: bash

   sudo apt-get install python3-tk

This installation process has been succesfully run in **Ubuntu 16.04** and **Debian 9**.

Windows set-up for developing
=============================
First of all, download the project source code from the repository with *git*. The project will be stored on a local folder named **Frequency-meter-APP**:

.. code-block:: bash
   
   cd <path-to-chosen-parent-folder>
   git clone https://github.com/jlrandulfe/Frequency-meter-APP.git

Install newest version of Python 3 for Windows (This has been tested with version 3.6.2. The python package manager pip should already be automatically installed when installing python. Otherwise install it. Also remember to add Pyhon to the system PATH varibles (Check that option during installation) so Windows command prompt can later find python interpreter and pip.
  
In cmd (Windows Command Prompt) create a virtual environment and, with the *pip* tool, install the required python packages for the project:

.. code-block:: bash

   # Install the virtual environment management library (Windows port); and set-up commands and OS environment
   pip3 install virtualenvwrapper-win
   #WORKON_HOME (the path to store environments) is by default %USERPROFILE%\Envs
   # Create a Python3 virtual environment and install the project dependencies
   mkvirtualenv <env-name>
   cd <path-to-chosen-parent-folder>/Frequency-meter-APP
   pip3 install -r requirements.txt

In windows TK is installed with the Python3 installer so it is already in the system.

If you want to modify the Qt interfaces (.ui files) you need to install Qt Creator (You must install Qt5 for Windows). In Linux Qt Creator is automatically installed when installing pyQt5 but in Windows it is not.

This installation process has been succesfully run in **Windows 7** and **Windows 10**.