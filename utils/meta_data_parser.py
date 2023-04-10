import pandas as pd


def mat_to_dict(file):
    meta_data_dict = {}

    # there is already a 'name' field included and 'celeb_names' is a duplicate.
    file.pop('celeb_names')
    for row in pd.DataFrame(file).to_dict('records'):
        meta_data_dict[row['full_path'][3:]] = row
    return meta_data_dict
