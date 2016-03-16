import fellow
import typecheck
from .data import sample_song_features

keys = ["fe_test_%04d.mp3" % i for i in xrange(1, 146)]
sol = {k: "blues" for k in keys}

@fellow.app.task(name="music.raw_features_predictions")
@typecheck.returns_dict("string", keys)
def raw_features_predictions():
    return sol


@fellow.app.task(name="music.all_features_predictions")
@typecheck.returns_dict("string", keys)
def all_features_predictions():
    return sol


@fellow.batch(name="music.all_features_model")
@typecheck.test_cases(record=sample_song_features)
@typecheck.returns("string")
def all_features_model(record):
    return "blues"
