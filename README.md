CSC-231 Lab Auto Grader
===================


This is a auto-grading script that uses simple diff to check students' assignment submission outputs with the reference output, designed for the instructors of CSC-231 (Programming for Engineers, MATLAB) at Cal Poly San Luis Obispo.

This auto-grading script is only effective if the students were instructed to match the output exactly to the smallest detail possible.

----------
New Features
-------------
Last update: Sunday, April 9, 2017

* This tool can now generate a reference solution from the given MATLAB source code. Place instructor solutions under `/solutions/source/`.
* If the source code to generate reference solution is not provided, default reference solutions under `/solutions/default/` will be used. See **Known Issues** below for more information about the default solutions.

Requirements
-------------
This script requires that you have the following installed on the machine in which it runs:

* Python 3.5 or later
* MATLAB R2016b or later, with Symbolic Math Toolkit
* Environment variable or alias to allow command-line `matlab` run in shell
* **OPTIONAL** a Virtual Machine or some other sandbox-like environment to run the script in, since this script runs arbitrary MATLAB code (student submissions).

In theory, this script should be cross-platform, but it was only tested on **macOS** and **Linux** (Xubuntu 16.04 LTS, to be exact).

How to Set it Up
-------------

Inner workings of this auto-grader are optimized based on the assumption that student submissions were downloaded from **PolyLearn** (Moodle-based course management system used at Cal Poly), unzipped, and copied into the working directory.

#### Things you should know about
* `dir_LM.dat` is a data file for MATLAB used by `generate_output.m`. In it, you should list *full path* for two directories: **results** and **submissions**, in that order. This serves as a list of working directories for a local-machine run.
* `dir_VM.dat` is a data file for MATLAB used by `generate_output_vm.m`. In it, you should list *full path* for two directories: **results** and **submissions**, in that order. This serves as a list of working directories for a virtual machine run.
* `diff_config.json` is a JSON file that holds some runtime configurations for the script. Only attribute you'll need to change in this file is `labs`, to select which labs to grade. By default, it is set to grade all non-plotting labs (excluding the final exam, denoted by number `0`).
* `diff.py` is the main script you'll run. Use the following command on your machine's console:
```bash
~$ python3 diff.py
```

#### Things that won't matter much to you
* `diff_adt.py` holds some abstract data types used by the script. you can mostly ignore this.
* `generate_solution.m` is a MATLAB script used to generate reference solutions based on the solution source code you provide.
* `generate_output.m` is a MATLAB script that actually runs student submissions to generate the output.
* `generate_output_vm.m` is an exact copy of `generate_output.m`. I use it to lazily have two environments I can run auto-grader in. If you're only going to have a single environment to use auto-grader in, you can ignore this as well. Following the usage shown below, you can trigger the use of this MATLAB script versus the other one:
```bash
~$ python3 diff.py -vm
```

How to Use
-------------
1. [Click here to download this tool (ZIP)](https://github.com/7imeout/CSC231-AutoGrader/archive/master.zip).
1. Once downloaded, unzip its content, preserving the existing directory structure.
1. You'll need to make some changes to a few files. Follow **How to Set it Up** guide above to get things set up.
1. Run the following command in shell:  ``` ~$ python3 diff.py```. Initial run will detect the lack of required working directory structures and run some setup without grading anything.
1.  I **strongly recommend** that you provide your lab solutions to generate the reference solution (to be used for comparison with student outputs). Place your MATLAB source code under `/solutions/source/`.
1. Download "ALL" student submissions as a ZIP archive from **PolyLearn**.
1. Unzip the archive, and place individual submission folders, usually named something like `Firstname_Lastname_123456_assignsubmission_file_` into the appropriate `labXX` directory under `/submissions/`.
1. Run the following command in shell:  ``` ~$ python3 diff.py [-vm] ```. This is to actually run auto-grade. `-vm` is optional.
1. When the script finishes execution without encountering any unexpected errors, you should see text files generated under `/results/` directory, and a grading result summarized in a CSV file under `/csv/`.


> **Note:**

> - Student submission that causes runtime error during MATLAB run will simply cause the student's output to include the MATLAB error message.
> - If a student's output matched the reference output 100%, **True** will be shown on the CSV. If there was *any* mismatch, **False** will be shown. If there was no submission for the given lab, no entry will be shown.
> - To further investigate the cause of any mismatches, I recommend using `diff`, or [diffchecker.com](https://diffchecker.com).

Known Issues
-------------
* Default reference outputs provided in `/solutions/default/` isn't necessarily correct for what your student outputs will be in the environment you are running this tool in. Using default reference outputs **most likely will** cause mismatches due to different formating.
> You can place your solution (MATLAB source code) into `/solutions/source/` for each lab you plan to grade. This tool will detect it and generate new reference solutions based on the source code provided.

* While generating reference solutions from the source code provided in `/solutions/source/`, MATLAB might display warnings. These are negligible.
> Warning displayed is due to the `delete(...)` function call that attempts to delete any existing reference solution.

* There's no feature to distinguish or separate students by class section.
> You can work around this by having multiple instances (copies) of this tool in separate directories, one per section, if desired.

* Students with the same first and last name will appear as a single student, with the grading result of the submission that appeared later overwriting the earlier result.
> You can work around this issue by manually renaming one of the student's directories to avoid same names.

Questions, Concerns, and Comments?
-------------
* Any improvements made to this script will be updated via **Git** (here).
* Please send any feedback to **doryu@calpoly.edu**.