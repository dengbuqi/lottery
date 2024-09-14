import os
import pandas as pd

def read_data(root_dir='../data', prefix='dlt_'): #prefix='dlt_' or 'ssq' or 'Powerball_'
    csv_files = [file for file in os.listdir(root_dir) if file.startswith(prefix) and file.endswith('.csv')]
    csv_files.sort()
    concatenated_data = pd.DataFrame()
    for file in csv_files:
        file_path = os.path.join(root_dir, file)
        data = pd.read_csv(file_path)
        concatenated_data = pd.concat([concatenated_data, data])
    return concatenated_data