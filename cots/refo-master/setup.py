#!/usr/bin/env python
import sys


def setup_python3():
    # Taken from "distribute" setup.py
    from distutils.filelist import FileList
    from distutils import dir_util, file_util, util, log
    from os.path import join, exists

    tmp_src = join("build", "src")
    # Not covered by "setup.py clean --all", so explicit deletion required.
    if exists(tmp_src):
        dir_util.remove_tree(tmp_src)
    log.set_verbosity(1)
    fl = FileList()
    for line in open("MANIFEST.in"):
        if not line.strip():
            continue
        fl.process_template_line(line)
    dir_util.create_tree(tmp_src, fl.files)
    outfiles_2to3 = []
    for f in fl.files:
        outf, copied = file_util.copy_file(f, join(tmp_src, f), update=1)
        if copied and outf.endswith(".py"):
            outfiles_2to3.append(outf)
    util.run_2to3(outfiles_2to3)
    # arrange setup to use the copy
    sys.path.insert(0, tmp_src)
    return tmp_src

kwargs = {}

if sys.version_info[0] >= 3:
    from setuptools import setup
    assert setup
    kwargs['use_2to3'] = True
    kwargs['src_root'] = setup_python3()
else:
    try:
        from setuptools import setup
        kwargs['test_suite'] = "nose.collector"
        assert setup
    except ImportError:
        from distutils.core import setup


config = dict(
    name="REfO",
    version="0.12",
    description="Regular expressions for objects",
    long_description=open('README.txt').read(),
    author="Rafael Carrascosa",
    author_email="rafacarrascosa@gmail.com",
    url="https://github.com/machinalis/refo",
    keywords=["regular expressions", "regexp", "re", "objects", "classes"],
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing",
        "Topic :: Utilities",
        ],
    packages=["refo"],
    **kwargs
)

setup(**config)
