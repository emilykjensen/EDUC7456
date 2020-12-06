import pandas as pd

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
