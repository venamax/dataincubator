import fellow
import typecheck

@fellow.app.task(name="spark.upvote_percentage_by_favorites")
@typecheck.returns("50 * (count, number)")
def upvote_percentage_by_favorites():
    return [(20, 0.9952153110047847)] * 50


@fellow.app.task(name="spark.user_answer_percentage_by_reputation")
@typecheck.returns("100 * (number, number)")
def user_answer_percentage_by_reputation():
    return [(7071, 0.9107142857142857)] * 100


@fellow.app.task(name="spark.user_reputation_by_tenure")
@typecheck.returns("100 * (count, number)")
def user_reputation_by_tenure():
    return [(118, 3736.5)] * 100

@fellow.app.task(name="spark.quick_answers_by_hour")
@typecheck.returns("24 * number")
def quick_answers_by_hour():
    return [0.] * 24


@fellow.app.task(name="spark.quick_answers_by_hour_full")
@typecheck.returns("24 * number")
def quick_answers_by_hour_full():
    return [0.] * 24

keys = ["vet_views", "vet_score", "vet_favorites", "vet_answers",
        "brief_views", "brief_score", "brief_favorites", "brief_answers"]

@fellow.app.task(name="spark.identify_veterans_from_first_post_stats")
@typecheck.returns_dict("number", keys)
def identify_veterans_from_first_post_stats():
    return {"vet_views": 0.,
            "vet_score": 0.,
            "vet_favorites": 0.,
            "vet_answers": 0.,
            "brief_views": 0.,
            "brief_score": 0.,
            "brief_favorites": 0.,
            "brief_answers": 0.
            }

@fellow.app.task(name="spark.identify_veterans_from_first_post_stats_full")
@typecheck.returns_dict("number", keys)
def identify_veterans_from_first_post_stats_full():
    return {"vet_views": 0.,
            "vet_score": 0.,
            "vet_favorites": 0.,
            "vet_answers": 0.,
            "brief_views": 0.,
            "brief_score": 0.,
            "brief_favorites": 0.,
            "brief_answers": 0.
            }

@fellow.app.task(name="spark.word2vec")
@typecheck.returns("25 * (string, number)")
def word2vec():
    return [("data.frame", 2.479299366496595)] * 25
