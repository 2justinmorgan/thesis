import defines
import commons


def store(session):
    commons.is_dir(defines.RECORDED_SESSIONS_DIR)

    for feature in session.features:
        outfile = open(f"{defines.RECORDED_SESSIONS_DIR}/{session.id}_{feature}", "w")
        outfile.write(f"{session.features[feature].records}")
        outfile.close()
