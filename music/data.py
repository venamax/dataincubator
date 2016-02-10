# flake8: noqa


import gzip
import dill

def load_sample_songs():
    with gzip.open('data.dill.gz') as ff:
        sample_songs =  dill.load(ff)
    return sample_songs