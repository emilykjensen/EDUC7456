import pandas as pd
import numpy as np

# make level 3 (school) file
# this file just contains schoolID, since we do not have any other school-level predictors
df = pd.read_csv('student-1718_after_additional_preprocess.csv')
schools = df['school_number_eoc']
schools_unique = schools.drop_duplicates()
schools_unique_sorted = schools_unique.sort_values()
schools_unique_sorted.name = 'schoolID'
schools_unique_sorted.to_csv('level3.csv',index=False,header=True)
print('There are {} unique schools in the dataset'.format(len(schools_unique_sorted)))
## There are 658 unique schools in the dataset

# make level 2 (student) file
# this file contains schoolID, studentID, and achievement scores at beginning (prior) and end (EOC) of the school year
students = df[['user_account','school_number_eoc','dev_scale_score_nq_c','scale_score_nq_c']]
students.columns = ['studentID','schoolID','prior','EOC']
students_sorted = students.sort_values(['schoolID','studentID'])
students_sorted.to_csv('level2.csv',index=False,header=True)
print('There are {} unique students in the dataset'.format(len(students_sorted)))
## There are 86916 unique students in the dataset

# make level 1 (survey) file
# this file contains schoolID, studentID, time of survey, survey answer, and some other survey info that might be of interest later
surveys = pd.read_csv('survey-answers-matched-scaled.csv')
surveys_filtered = surveys[['user_id','survey_id','timestamp_created','survey_question','survey_valence','survey_answer_unipolar']]
surveys_filtered.columns = ['studentID','surveyID','surveyTime','surveyEmotion','emotionValence','surveyResponse']
surveys_answered = surveys_filtered.loc[surveys_filtered['surveyResponse'] > 0]
surveys_merged = surveys_answered.merge(students_sorted, how='inner', on='studentID')
surveys_merged['surveyTime'] = pd.to_datetime(surveys_merged['surveyTime'], format='%Y-%m-%d %H:%M:%S')
first_survey = min(surveys_merged['surveyTime'])
surveys_merged['monthStart'] = (surveys_merged['surveyTime'].dt.year - first_survey.year) * 12 + (surveys_merged['surveyTime'].dt.month - first_survey.month)
surveys_merged['monthEnd'] = surveys_merged['monthStart'] - max(surveys_merged['monthStart'])
surveys_sorted = surveys_merged.sort_values(['schoolID','studentID','surveyTime'])
surveys_sorted.to_csv('level3.csv',index=False,header=True)
print('There are {} total surveys'.format(len(surveys_sorted)))
## There are 89164 total surveys
