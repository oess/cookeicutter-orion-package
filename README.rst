OpenEye Cube/Floe Package CookieCutter Template
===============================================

A `Cookiecutter`_ template for Orion packages containing Cubes and Floes.

Support
-------

For all questions regarding the usage of this CookieCutter template, please contact
`OpenEye Support`_.

Features
--------
* Sets up skeleton of an Orion package containing Cubes and Floes
* Simple example Cube and Floe
* Testing setup using `PyTest`_ including working test for the example cube and floe
* Automatic documentation generation (using `Sphinx`_) for cubes and floes
* Commands for running tests, building docs, and packaging using `Invoke`_
* Version configuration via storing the version only in the module's ``__init__.py`` file


Requirements
------------
* Python 3.8 or higher. We recommend starting with a clean `conda`_ environment, which can be created and activated as: 
    ::

        conda create -n vir_env python=3.8  
        conda activate vir_env


* `Cookiecutter`_

* Access to OpenEye’s Python package server, `Magpie`_. If you are a licensed Orion user and don't have access, please contact `OpenEye Support`_. Follow the instructions there to configure access to Orion python packages via your ``pip.conf`` file.

* A `configured Orion profile`_ to communicate with Orion server. After 'pip install -e .' step below, profile can be configured as: (needs Orion login credentials)
    ::

        ocli --profile=default config profile 

  

Setup
-----

#. `Install cookiecutter`_, usually via running ``pip install cookiecutter``

#. Run ``cookiecutter  gh:oess/cookiecutter-orion-package``

    **Note:** running cookiecutter directly against the GitHub repository requires ``git`` to be locally installed. To install without requiring ``git``,
    download the ZIP file from `GitHub`_ and run  ``cookiecutter cookiecutter-orion-package-master.zip``

#. This will generate a directory with the name you provided as the project_slug in the cookiecutter setup. Switch into the directory

    ::

        cd <project_slug>


#. Next install all requirements and development requirements:

    ::

        pip install -e .
        pip install -r requirements_dev.txt



Commands
--------


Once all dependencies are installed, you should be able to use invoke to build a version of the package for upload to Orion (the tar.gz will be in the dist directory):

::

    invoke package

Tests are set up for the cube and floe that are included, they can be run locally:

::

    invoke test-all

Command to just test cubes

::

    invoke test-cubes

Command to just test floes

::

    invoke test-floes

To clean up generated documentation and packaging files, run:

::

    invoke clean

You can also selectively clean only documentation files as follows:

::

    invoke clean-docs



Output Skeleton
---------------

The following directory structure will be created by the ``cookiecutter``, the items marked in ``{{ }}`` will be replaced by your choices
upon completion::

    {{cookiecutter.project_slug}}/              <-- Top directory for your Project.
    ├── MANIFEST.in
    ├── README.md                               <-- README with your Project Name and description.
    ├── docs                                    <-- Docs subdirectory set up for automatic documentation of cubes and floes.
    │   ├── Makefile
    │   ├── make.bat
    │   └── source
    │       ├── _static
    │       ├── _templates
    │       ├── conf.py
    │       └── index.rst
    ├── floes                                   <-- Subdirectory where all floes should be placed.
    │   └── example_floe.py                           <-- An example floe.
    ├── manifest.json                           <-- Manifest for Orion.
    ├── requirements_dev.txt                    <-- Requirements file for development of this package.
    ├── setup.py                                <-- Python file for creating a python package
    ├── tasks.py                                <-- Python file with defined tasks for building docs, running tests, and building the package.
    ├── tests                                   <-- Subdirectory for testing of cubes and floes.
    │   ├── floe_tests                          <-- Subdirectory for floe tests
    │   │   └── test_example_floe.py            <-- Example floe test to run locally or in Orion
    │   ├── test_data
    │   │   └── 10.ism
    │   └── test_example_cube.py                <-- An example unit test for the included cube.
    └── {{cookiecutter.module_name}}            <-- Subdirectory of the package for the python module. All cubes should go in here.
        ├── __init__.py
        └── example_cube.py                     <-- An example cube.

..



.. _Cookiecutter: https://cookiecutter.readthedocs.io/
.. _PyTest: https://docs.pytest.org/
.. _Sphinx: http://www.sphinx-doc.org/
.. _Invoke: http://www.pyinvoke.org/
.. _conda: https://conda.io/docs/user-guide/overview.html
.. _magpie: https://magpie.eyesopen.com
.. _OpenEye Support: mailto:support%40eyesopen.com
.. _Install cookiecutter: https://cookiecutter.readthedocs.io/en/latest/installation.html
.. _GitHub: https://github.com/oess/cookiecutter-orion-package
.. _configured Orion profile: https://docs.eyesopen.com/orion-developer/modules/orion-client/docs/quickstart.html#installing-orion-client
