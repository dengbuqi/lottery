import os

def find_last_year(root_dir, prefix): # prefix = 'ssq_' or 'dlt_'
    # max_file = None
    max_size = 0
    for file_name in os.listdir(root_dir):
        if file_name.startswith(prefix) and file_name.endswith('.csv'):
            # file_path = os.path.join(root_dir, file_name)
            file_number = int(file_name.split(prefix)[1].split('.csv')[0])
            if file_number > max_size:
                # max_file = file_path
                max_size = file_number
    return max_size