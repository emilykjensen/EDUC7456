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
