from .db import session
from .models import Vacancies


def add_vacancy(data: dict):
    if not check_vacancy(data):
        
        vacancy = Vacancies(company=data["company"],
                            job_title=data["job_title"],
                            job_link=data["job_link"],
                            employee=data["employee"],
                            date=data["date"])
        session.add(vacancy)
        session.commit()
        
def check_vacancy(data: dict):
    vacancy = session.query(Vacancies).filter_by(job_link=data["job_link"]).first()
    if vacancy:
        return True
    else:
        return False