import defines
import commons


def store(session):
    commons.is_path(defines.RECORDED_SESSIONS_DIR, exit_on_fail=True, exit_code=1)

    for feature in session.features:
        outfile = open(f"{defines.RECORDED_SESSIONS_DIR}/{session.id}_{session.user}_{feature}", "w")
        outfile.write(f"{session.features[feature].records}")
        outfile.close()
