import models
from org_files_backend_settings.database import get_db_session_to_variable


def load_organisations():
    db = get_db_session_to_variable()

    for i in range(1, 6):
        org_obj = models.Organisation(name=f'Org{i}')
        db.add(org_obj)
    db.commit()
    db.close()


if __name__ == "__main__":
    load_organisations()
