# (C) 2018 OpenEye Scientific Software Inc. All rights reserved.
#
# TERMS FOR USE OF SAMPLE CODE The software below ("Sample Code") is
# provided to current licensees or subscribers of OpenEye products or
# SaaS offerings (each a "Customer").
# Customer is hereby permitted to use, copy, and modify the Sample Code,
# subject to these terms. OpenEye claims no rights to Customer's
# modifications. Modification of Sample Code is at Customer's sole and
# exclusive risk. Sample Code may require Customer to have a then
# current license or subscription to the applicable OpenEye offering.
# THE SAMPLE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED.  OPENEYE DISCLAIMS ALL WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. In no event shall OpenEye be
# liable for any damages or liability in connection with the Sample Code
# or its use.

import os
import sys
import shutil
from json import loads, dump
from invoke import task, run
from setuptools import convert_path

pty = False
if sys.platform != "win32":
    pty = True


@task
def flake8(ctx):
    run("flake8 --max-line-length 100 {{cookiecutter.module_name}}")


@task
def update_manifest(ctx):
    """
    Updates manifest.json with the correct version of {{cookiecutter.project_slug}}
    """
    spec = loads(open("manifest.json", "r").read())
    sys.path.append(os.path.dirname(__file__))
    import {{cookiecutter.module_name}}
    spec["version"] = {{cookiecutter.module_name}}.__version__
    dump(spec, open("manifest.json", "w"))


@task
def package(ctx):
    """
    Create package
    """
    # Create the Orion packaging files
    _make_reqs_file()
    update_manifest(ctx)
    # Run standard python packaging, which will include the Orion packaging files we just created
    run("python setup.py sdist --formats=gztar")

    # Removed the Orion packaging files now that we are done with packaging
    _clean_orion_package_files()


@task
def docs(ctx):
    curdir = os.getcwd()
    run("cube_doc {{cookiecutter.module_name}} docs/source")
    run("floe_doc {{cookiecutter.module_name}} floes docs/source")
    os.chdir("docs")
    if sys.platform == "win32":
        run("make.bat html")
    else:
        run("make html")
    os.chdir(curdir)


# need to clean out .pyc files to share a directory
# with both Windows and Bash/WSL
@task
def clean_pyc(ctx):
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".pyc"):
                filename = os.path.join(root, file)
                if os.path.exists(filename):
                    os.unlink(filename)


@task
def flint(ctx):
    run("floe lint floes/")


@task
def test_cubes(ctx, opts="-s"):
    """
    run cube tests
    """
    run("python -m pytest --tb=native -m 'not floetest' {}".format(opts), pty=pty)


@task
def test_floes(ctx, opts=""):
    """
    run tests
    """
    # clean_pyc(ctx)
    run("python -m pytest --tb=native -m 'floetest' {} ".format(opts), pty=pty)


@task
def test_all(ctx, profile="default", opts=""):
    """
    run cube tests and then run floe tests locally and then floe tests against Orion
    """
    test_cubes(ctx, opts)
    test_floes(ctx, opts)
    test_orion(ctx, profile, opts)


@task
def test_orion(ctx, profile="", opts=""):
    """
    run tests
    """

    if profile == "":
        if "ORION_PROFILE" in os.environ:
            profile = os.getenv("ORION_PROFILE")
        else:
            profile = "default"
    print("Using Orion Profile: {}".format(profile))
    clean_pyc(ctx)
    clean(ctx)
    update_manifest(ctx)
    _make_reqs_file()
    if sys.platform != "win32":
        run(
            "ORION_PROFILE={} python -m pytest -v -s --tb=native  -m floetest --orion {}".format(
                profile, opts
            ),
            pty=pty,
        )
    elif "ORION_PROFILE" not in os.environ:
        os.environ["ORION_PROFILE"] = profile
        run(
            "python -m pytest -v -s --tb=native  -m floetest --orion {} ".format(opts),
            pty=pty,
        )
        os.environ["ORION_PROFILE"] = ""
    else:
        run(
            "python -m pytest -v -s --tb=native  -m floetest --orion {} ".format(opts),
            pty=pty,
        )
    _clean_orion_package_files()


@task
def serve_docs(ctx):
    docs(ctx)
    curdir = os.getcwd()
    os.chdir("docs/build/html")
    run("python -m http.server")
    os.chdir(curdir)


@task
def clean(ctx):
    """
    Clean up doc and package builds
    """
    clean_pyc(ctx)
    shutil.rmtree("dist", ignore_errors=True)
    shutil.rmtree("build", ignore_errors=True)
    egg_path = "{}.egg-info".format("{{cookiecutter.project_slug}}".replace("-", "_"))
    if os.path.isfile(egg_path):
        os.remove(egg_path)
    elif os.path.isdir(egg_path):
        shutil.rmtree(egg_path)


@task
def clean_docs(ctx):
    doc_dir = "docs/build/html"
    _clean_out_dir(doc_dir)
    # _clean_out_dir("docs/source/floes")
    _clean_out_dir("docs/source/cubes")

    if os.path.isdir("docs/build/doctrees"):
        shutil.rmtree("docs/build/doctrees")


def _clean_out_dir(dir_path):
    if os.path.isdir(dir_path):
        for the_file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(e)


def _make_reqs_file(reqs_filename="orion-requirements.txt"):
    requirements = loads(
        run("python setup.py --requires", hide="both").stdout.strip("\n\r")
    )

    # Create the Orion packaging files
    reqs_path = convert_path("./{}".format(reqs_filename))

    with open(reqs_path, "w") as reqs_file:
        for req in requirements:
            reqs_file.write(req)
            reqs_file.write("\n")


def _clean_orion_package_files(reqs_filename="orion-requirements.txt"):
    # Create the Orion packaging files
    reqs_path = convert_path("./{}".format(reqs_filename))
    if os.path.isfile(reqs_path):
        os.remove(reqs_path)
