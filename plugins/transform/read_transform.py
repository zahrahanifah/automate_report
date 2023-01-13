import pandas as pd
import glob
import os

# Mendefinisikan home directory di laptop kita
HOME = os.path.expanduser("~")

# append files because it is separate within certain period
def __append_files(extension, directory):
    
    #store multiple files directory into a list using iteration/looping
    folder = glob.glob('{directory}/*.{ext}'.format(directory=directory, ext=extension))
    all_filenames = []
    for file in folder:
        all_filenames.append(file)

    #read csv and concat it into one single dataframe using iteration
    combined_csv = []

    for filename in all_filenames:
        df = pd.read_csv(filename)
        combined_csv.append(df)
        
    combined_csv = pd.concat(combined_csv)

    return combined_csv

# do transform and summarize the data
def run_transform(folder):
    data = __append_files(
        'csv', folder)

    #generate new column with conditional 
    data['status'] = ['Closed' if x =='Closed' else 'Open' for x in data['ticket_status']]
    
    print(data)
    return data

if __name__ == '__main__':
    run_transform('C:/Users/zahra.hanifah/Downloads/Zahra/000 Learning/DE Bootcamp/automate_report/data')