import pandas as pd
import numpy as np

# make level 3 (school) file
# this file just contains schoolID, since we do not have any other school-level predictors
df = pd.read_csv('student-1718_after_additional_preprocess.csv')
schools = df['school_number_eoc']
schools_unique = schools.drop_duplicates()
schools_unique_sorted = schools_unique.sort_values()
schools_unique_sorted.name = 'school'

# make level 2 (student) file
# this file contains schoolID, studentID, and achievement scores at beginning (prior) and end (EOC) of the school year
students = df[['user_account','school_number_eoc','dev_scale_score_nq_c','scale_score_nq_c']]
students.columns = ['student','school','prior','EOC']
students_sorted = students.sort_values(['school','student'])

# make level 1 (survey) file
# this file contains schoolID, studentID, time of survey, survey answer, and some other survey info that might be of interest later
surveys = pd.read_csv('survey-answers-matched-scaled.csv')
surveys_filtered = surveys[['user_id','survey_id','timestamp_created','survey_question','survey_valence','survey_answer_unipolar']]
surveys_filtered.columns = ['student','survey','time','emotion','valence','answer']
surveys_answered = surveys_filtered.loc[surveys_filtered['answer'] > 0]
surveys_merged = surveys_answered.merge(students_sorted, how='inner', on='student')
surveys_merged = surveys_merged.drop(['prior','EOC'], axis=1)
surveys_merged['time'] = pd.to_datetime(surveys_merged['time'], format='%Y-%m-%d %H:%M:%S')
first_survey = min(surveys_merged['time'])
surveys_merged['monthS'] = (surveys_merged['time'].dt.year - first_survey.year) * 12 + (surveys_merged['time'].dt.month - first_survey.month)
surveys_merged['monthE'] = surveys_merged['monthS'] - max(surveys_merged['monthS'])
surveys_sorted = surveys_merged.sort_values(['school','student','time'])

# make sure there are the same number of distinct students and schools in each file
# some of these were dropped when matching students with schools and surveys with students
students_sorted = students_sorted.loc[students_sorted['student'].isin(surveys_sorted['student'])]
students_sorted = students_sorted.loc[students_sorted['school'].isin(surveys_sorted['school'])]
schools_unique_sorted = schools_unique_sorted.loc[schools_unique_sorted.isin(surveys_sorted['school'])]

# save everything to csv
surveys_sorted.to_csv('level1.csv',index=False,header=True)
print('There are {} total surveys'.format(len(surveys_sorted)))
## There are 89164 total surveys
students_sorted.to_csv('level2.csv',index=False,header=True)
print('There are {} unique students in the dataset'.format(len(students_sorted)))
## There are 42053 unique students in the dataset
schools_unique_sorted.to_csv('level3.csv',index=False,header=True)
print('There are {} unique schools in the dataset'.format(len(schools_unique_sorted)))
## There are 590 unique schools in the dataset
