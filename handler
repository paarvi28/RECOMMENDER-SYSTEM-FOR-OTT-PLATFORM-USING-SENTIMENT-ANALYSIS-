from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
import datetime
from models.user_model import User, EmailTracker

################################################# User Creation ############################################
def create_user(user_details, engine):
    status_code = None
    description = None
    try:
        Session = sessionmaker(bind=engine)
        session = Session()
        new_user = User(**user_details)
        session.add(new_user)
        session.commit()
        session.close()
        status_code = 201
        description = "User Created"
    except IntegrityError:
        session.rollback()
        status_code = 400
        description = "User already exists"
    except Exception as e:
        session.rollback()
        status_code = 500
        description = str(e)
    finally:
        session.close()
    return {"status_code": status_code, "description": description}

################################################# Get User Details ########################################
def get_user_details(username, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user
    except Exception as e:
        session.rollback()
        session.close()
        return None

################################################# Get Hashed Password #####################################
def get_hashed_password(username, engine):
    user = get_user_details(username, engine)
    return user.password if user else None

################################################# Update User Details #####################################
def update_user_details(username, updated_user_details, engine):
    status_code = None
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            user.first_name = updated_user_details['first_name']
            user.last_name = updated_user_details['last_name']
            user.password = updated_user_details['password']
            user.account_updated = datetime.datetime.now()
            session.commit()
            status_code = 204  # User Updated
        else:
            status_code = 404  # User Not found
    except Exception as e:
        session.rollback()
        status_code = 500
    finally:
        session.close()
    return {"status_code": status_code}

################################################# Verify User ##############################################
def verify_user(id, engine):
    status_code = None
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        user = session.query(User).filter_by(id=id).first()
        if user:
            user.verified = True
            session.commit()
            status_code = 200  # User Verified
        else:
            status_code = 404  # User Not found
    except Exception as e:
        session.rollback()
        status_code = 500
    finally:
        session.close()
    return {"status_code": status_code}

################################################# Track Emails ############################################
def get_email_tracker_details(token, engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        email_tracker = session.query(EmailTracker).filter_by(verification_token=token).first()
        session.close()
        return email_tracker.expire_time if email_tracker else None
    except Exception as e:
        session.rollback()
        session.close()
        return None
