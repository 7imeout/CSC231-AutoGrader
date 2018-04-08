CSC-231 Lab Auto Grader
===================

This tool was created for the instructors of CSC-231 (Programming for Engineers, MATLAB) at Cal Poly State University, San Luis Obispo.

This is a auto-grading script that uses Levenshtein distance (new) to grade students' assignment submission outputs against the reference. 

This auto-grading script is mostly effective if the students were instructed to match the output exactly to the smallest detail possible.

----------
New Features
-------------
Latest update: Sunday, April 8, 2018

* All-or-nothing scheme is gone! Now, Levenshtein distance (edit distance) is used to give partial credit. Edit distance is subtracted from the length of the reference output, such that the edit distance equal to or greater than the length of the distance results in no credit.
* This tool now generates separate CSV files for each section of the course being taught (based on the roster provided), as well as separate CSVs for each individual lab assignment.
* All of the separately generated CSVs allow for PolyLearn-compatibility. You should be able to use the output of this program to upload grades directly to PolyLearn's grade book.

Past update: Sunday, April 9, 2017

* This tool can now generate a reference solution from the given MATLAB source code. Place instructor solutions under `/solutions/source/`.
* If the source code to generate reference solution is not provided, default reference solutions under `/solutions/default/` will be used. See **Known Issues** below for more information about the default solutions.

Requirements
-------------
This script requires that you have the following installed on the machine in which it runs:

* Python 3.5 or later
* MATLAB R2016b or later, with Symbolic Math Toolkit
* Environment variable or alias to allow command-line `matlab` run in shell
* **OPTIONAL** a Virtual Machine or some other sandbox-like environment to run the script in, since this script runs arbitrary MATLAB code (student submissions).

In theory, this script should work on all *nix based environment, but it was only tested on **macOS** and **Linux** (Xubuntu 16.04 LTS, to be exact).

How to Set it Up
-------------

Inner workings of this auto-grader are dependent on the assumption that student submissions were downloaded from **PolyLearn** (Moodle-based course management system used at Cal Poly), unzipped, and copied into the working directory.

#### Things you should know about
* `diff.py` is the main script you'll run. Use the following command on your machine's console:
    ```bash
    ~$ python3 diff.py
    ```
* `dir_LM.dat` is a data file for MATLAB used by `generate_output.m`. In it, you should list *full path* for two directories: **results** and **submissions**, one path per line, in that order. This serves as a list of working directories for a local-machine run.
* `dir_VM.dat` is a data file for MATLAB used by `generate_output_vm.m`. In it, you should list *full path* for two directories: **results** and **submissions**, one path per line, in that order. This serves as a list of working directories for a virtual machine run.
* `diff_config.json` is a JSON file that holds some runtime configurations for the script. There are a few attribute you might want to change in this file to match your course and grading scheme:

    * `labs` attribute is a list of integers indicating which lab assignments you will be grading. Place a `1` for `lab01.m`, `2` for `lab02.m`, and so on. Use `0` to grade `final.m`.
    * `score_out_of` attribute is, just like the name suggests, the max score achievable for each lab. It's a single floating point number to be applied to all lab assignments.
    * `roster_paths` is a list of `[<section_id>, <section_roster_path>]`'s. 
        * Using the roster functionality is optional. Keep this as an empty list (`[]`) if you do not wish to use this feature.
        * Nevertheless, it is recommended that you do use this feature if you are teaching more than a single section of CSC-231, or wish to generate CSV files you can import directly into PolyLearn to upload the grades.
        * `<section_id>` is a string correcponding to however you wish to identify your sections. _**e.g.**_ `"Tue/Thur"` or `"2pm"` works.
        * `<section_roster_path>` is a file path to the CSV of the roster for your section. Obtain this roster by using the grades "export" functionality on PolyLearn. First _**three**_ columns of this CSV must contain `First` (column 0) and `Last` (column 1) name of the student, as well as their `Email Address` (column 2). The first row of the CSV is assumed to be the header. The rest is simply ignored by the tool.
    * You can change the other attributes as you see fit, but they need not be for this tool to function correctly.


#### Things that won't matter much to you
* `diff_adt.py` holds some abstract data types used by the script. you can mostly ignore this.
* `generate_solution.m` is a MATLAB script used to generate reference solutions based on the solution source code you provide.
* `generate_output.m` is a MATLAB script that actually runs student submissions to generate the output.
* `generate_output_vm.m` is an exact copy of `generate_output.m`. I use it to lazily have two environments I can run auto-grader in. If you're only going to have a single environment to use auto-grader in, you can ignore this as well. Following the usage shown below, you can trigger the use of this MATLAB script versus the other one:
    ```bash
    ~$ python3 diff.py -vm
    ```

How to Use This Auto Grader
-------------
1. [Click here to download this tool (ZIP)](https://github.com/7imeout/CSC231-AutoGrader/archive/master.zip).
1. Once downloaded, unzip its content, preserving the existing directory structure.
1. You'll need to make some changes to a few files. Follow **How to Set it Up** guide above to get things set up. **Pay close attention to the mention of `roster_paths` attribute inside of `diff_config.json` if you are teaching more than a single section of CSC-231.**
1. After the setup, run the following command in shell:  ``` ~$ python3 diff.py```. Initial run will detect the lack of required working directory structures and run some setup without grading anything.
1.  I **strongly recommend** that you provide your lab solutions to generate the reference solution (to be used for comparison with student outputs). Place your MATLAB source code under `/solutions/source/`.
1. Download "ALL" student submissions as a ZIP archive from **PolyLearn**.
1. Unzip the archive, and place individual submission folders, usually named something like `Firstname_Lastname_123456_assignsubmission_file_` into the appropriate `labXX` directory under `/submissions/`.
1. Run the following command in shell:  ``` ~$ python3 diff.py [-vm] ```. This is to actually run auto-grade. `-vm` is optional.
1. When the script finishes execution without encountering any unexpected errors, you should see text files generated under `/results/` directory, and a grading result summarized in a CSV file under `/csv/` (or in whatever directories you have specified in `diff_config.json`).


   > **Note:**
   > 
   > - Student submission that causes runtime error during MATLAB run will simply cause the student's output to include the MATLAB error message.
   > - Formula used to calculate the score is: `max(0, (length_of_referene_solution - edit_distance) / length_of_referene_solution * score_out_of)`
   > - To further investigate the cause of any mismatches, I recommend using `diff` (UNIX), or [diffchecker.com](https://diffchecker.com).

Known Issues and Workarounds
-------------
* Default reference outputs provided in `/solutions/default/` isn't necessarily correct for what your student outputs will be in the environment you are running this tool in. Using default reference outputs **most likely will** cause mismatches due to different formating.
    > You can place your solution (MATLAB source code) into `/solutions/source/` for each lab you plan to grade. This tool will detect it and generate new reference solutions based on the source code provided.

* MATLAB might display warnings while generating reference solutions from the source code provided in `/solutions/source/`. These are negligible.
    > Warning displayed is due to the `delete(...)` function call that attempts to delete any existing reference solution.

* Students with the same first and last name will appear as a single student, with the grading result of the submission that appeared later overwriting the earlier result.
    > You can work around this issue by manually renaming one of the student's directories to avoid same names (Sorry).

Questions, Concerns, and Comments?
-------------
* Any improvements made to this script will be updated via **Git** (here).
* Please send any feedback to **doryu@calpoly.edu**.