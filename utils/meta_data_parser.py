import pandas as pd
import numpy as np


def mat_to_dict(file):
    imdb_dict = {}

    for n in file.dtype.names:
        if n != 'face_location':
            imdb_dict[n] = np.hstack(file[n][0, 0].flatten())
        else:
            imdb_dict[n] = [x[0] for x in np.hstack(file[n][0, 0])]

    imdb_frame = pd.DataFrame({k: pd.Series(v) for k, v in imdb_dict.items() if k not in ['celeb_names']})

    imdb_celeb = pd.DataFrame({k: v for k, v in imdb_dict.items() if k in ['celeb_names']})

    imdb_meta_data = imdb_frame.merge(imdb_celeb, how='inner', left_on='name', right_on='celeb_names',
                                      validate='m:1', indicator=True)

    if imdb_meta_data['_merge'].value_counts()['left_only'] != 0:
        raise Exception('some of the merged elements are left_only')
    elif imdb_meta_data['_merge'].value_counts()['right_only'] != 0:
        raise Exception('some of the merged elements are right_only')
    else:
        pass

    imdb_meta_data = imdb_meta_data.drop('_merge', axis=1)

    meta_data_each_image = []

    for i, x in imdb_meta_data.iterrows():
        meta_data_each_image.append(x.to_dict())

    return meta_data_each_image