from databases.init import *
def create_application(Application: Base):
    from models.application_model import ApplicationModel
    App = ApplicationModel(
        user_id=Application.user_id,
        name=Application.name,
        category=Application.category,
        phone=Application.phone,
        comment=Application.comment,
    )
    session.add(App)
    session.commit()
    return App.id

def get_applications_by_user(user_id):
    from models.application_model import ApplicationModel
    applications = session.query(ApplicationModel).filter_by(user_id=user_id).all()
    return applications

def get_all_applications_pending():
    from models.application_model import ApplicationModel
    applications = session.query(ApplicationModel).filter_by(status='pending').all()
    return applications


def delete_application(application_id):
    from models.application_model import ApplicationModel
    application = session.query(ApplicationModel).get(application_id)
    if application:
        session.delete(application)
        session.commit()
        return True
    return False