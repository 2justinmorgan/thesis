import sys


def format_print(features_obj):
    for feature in features_obj:
        print(feature)
        for stat in features_obj[feature]["stats"]:
            val = features_obj[feature]["stats"][stat]
            sys.stdout.write(f" {stat}:")
            if type(val) == list:
                for e in val:
                    e = round(e, 2)
                    sys.stdout.write(f"{e} ")
            else:
                val = round(val, 2)
                sys.stdout.write(f"{val}")
        print()
