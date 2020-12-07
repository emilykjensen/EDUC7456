# EDUC7456
Final project code for EDUC 7456 (Multilevel Models) class.

The data for this project is not publicly available as it contains sensitive student information.

# What is contained here
- python script `make_leveled_files.py` extracts the data into 3 leveled csv files

# Steps to recreate the results
- obtain `student-1718_after_additional_preprocess.csv` data
- obtain `survey-answers-matched-scaled.csv` data
- run `make_leveled_files.py` to create `level1.csv`, `level2.csv`, and `level3.csv`
- load csv files into RStudio
- save each as an SAV file (using haven library), such as `write_sav(level1, 'level1.sav')`
- transfer files to Citrix and build MDM file
  + L3 ID = `school`
  + L2 ID = `student`
  + see uploaded output files
- run 4 models, results uploaded in output folder
