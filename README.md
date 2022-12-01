SMAC Test Bench GUI Toolkit
============================

Introduction
------------

This directory contains a collection of Graphical User Interfaces (GUIs) based on the QGIS plugin platform. The GUIs are dialog-based user interfaces designed in Qt-5. The QGIS plugins platform supports the Python programming language, and as a result the SMAC GUI Toolkit is written in Python 3.7. 


How Does It Work?
-----------------

The Python-based QGIS plugins are designed as wrappers for the C++ software modules for SMACT. The QGIS plugins accept user input through the GUI dialogs, then pass on these input parameters to the C++ command line.


Requirements
------------

The following pre-requisites must be satisfied to install and use the plugins.

* [QGIS](https://www.qgis.org/da/site/forusers/download.html) version 3.14 or newer
	* Version 3.16/3.22 long-term release is preferred for stability

To build documentation (optional), the following additional software are required.

* [Doxygen](https://www.doxygen.nl/index.html) v 1.8.18 or newer
* [doxypypy](https://github.com/Feneric/doxypypy) v 0.8.8 or newer
* [LaTex](https://www.latex-project.org/get/) (optional) to create a PDF document


Installation
-------------

The plugins are installed in three steps: 
1. Install QGIS
2. Deploy/Install plugins
3. Activate/Enable plugins in QGIS

Please follow the instructions provided in the ![user manual][1] to install the plugins.


Post-Installation
-----------------

The installation will create menu items in QGIS, named `Image Registration` and `ATDR`. These will have sub-menu items corresponding to the different software modules delivered under SMACT.

To use these plugins, the location of the C++ software executables (`*.exe`) must be specified to the plugins. To specify the location, first launch the `Image Registration > Settings Configuration` plugin, then click the button [...] and select the folder (called `qgis-exes`).

The C++ software can be located anywhere on the same computer. If using the installer, `setup.cmd` version 0.3 or newer, the software will typically be placed at `C:\OSGeo4W64\smact`. In older versions, the installer will *NOT* copy the downloaded C++ software. In either case, users can manually copy all the EXE and DLL files to any folder on the computer, and select that folder from the `Image Registration > Settings Configuration` plugin dialog.


References
-----------

[1]: AUG Signals, "SMACT UI Installation Manual.pdf", August 2021

