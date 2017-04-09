CSC-231 Lab Auto Grader
===================


This is a auto-grading script that uses simple diff to check students' assignment submission outputs with the reference output, designed for the instructors of CSC-231 (Programming for Engineers, MATLAB) at Cal Poly San Luis Obispo.

This auto-grading script is only effective if the students were instructed to match the output exactly to the smallest detail possible.

----------
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
* `diff.py` is the main script you'll run. Use the following command on your machine's console: 
```bash
~$ python3 diff.py
```
* `dir_LM.dat` is a data file for MATLAB used by `generate_output.m`. In it, you should list *full path* for two directories: **results** and **submissions**, in that order. This serves as a list of working directories for a local-machine run.
* `dir_VM.dat` is a data file for MATLAB used by `generate_output_vm.m`. In it, you should list *full path* for two directories: **results** and **submissions**, in that order. This serves as a list of working directories for a virtual machine run.
* `diff_config.json` is a JSON file that holds some runtime configurations for the script. Only attribute you'll need to change in this file is `labs`, to select which labs to grade. By default, it is set to grade all non-plotting labs (excluding the final exam).


#### Things that won't matter much to you
* `diff_adt.py` holds some abstract data types used by the script. you can mostly ignore this.
* `generate_output.m` is a MATLAB script that actually runs student submissions to generate the output.
* `generate_output_vm.m` is an exact copy of `generate_output.m`. I use it to lazily have two environments I can run auto-grader in. If you're only going to have a single environment to use auto-grader in, you can ignore this as well. Following the usage shown below, you can trigger the use of this MATLAB script versus the other one:
```bash
~$ python3 diff.py -vm
```

How to Use it
-------------
1. Download "ALL" student submissions as a ZIP archive from **PolyLearn**.
2. Unzip the archive, and place individual submission folders, usually named something like `Firstname_Lastname_123456_assignsubmission_file_` into the appropriate `labXX` directory under `/submissions`.
3. Run the following command in shell:  ``` ~$ python3 diff.py [-vm] ```
4. The script should run, and when it finishes without encountering any unexpected errors, you should see text files generated under `/results` directory, and a grading result summarized in a CSV file under `/csv`.


> **Note:**

> - Student submission that causes runtime error during MATLAB run will simply cause the student's output to include the MATLAB error message.
> - If a student's output matched the reference output 100%, **True** will be shown on the CSV. If there was *any* mismatch, **False** will be shown. If there was no submission for the given lab, no entry will be shown.
> - To further investigate the cause of any mismatches, I recommend using `diff`, or [diffchecker.com](https://diffchecker.com)

Known Issues
-------------
* Default reference outputs provided in `/solutions` isn't necessarily correct for what your student outputs will be in the environment you are running this tool in. Using default reference outputs **will** cause mismatches due to different formating.
> I **strongly recommend** that you generate your own reference outputs using your lab solution in the environment you'll be grading in. Feature to automatically generate reference output given the solution MATLAB files will be added soon ...

* There's no feature to distinguish or separate students by class section.
> You can work around this by having multiple instances (copies) of this tool in separate directories, one per section, if desired.

* Students with the same first and last name will appear as a single student, with the grading result of the submission that appeared later overwriting the earlier result.
> You can work around this issue by manually renaming one of the student's directories to avoid same names.

Questions, Concerns, and Comments?
-------------
* Any improvements made to this script will be updated via **Git** (here).
* Please send any feedback to **doryu@calpoly.edu**.