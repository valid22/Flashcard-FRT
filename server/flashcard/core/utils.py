from typing import Union
from flask import session, redirect, url_for
from flashcard.models.schema import User, Deck
from flashcard.models.error import APIException
from flashcard.models.error.user import UserNotFound, SessionExpired
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from io import BytesIO
import pandas as pd

def get_current_user_id() -> Union[int, None]:
    """Returns the current session's user id .

    Returns:
        Union[int, None]: user id
    """
    
    return session.get('user_id', None)

def get_current_user() -> User:
    """Get the current user object.

    Raises:
        APIException: SessionExpired
        APIException: UserNotFound

    Returns:
        User: User mobject
    """

    uid = get_current_user_id()
    
    if uid is None:
        raise APIException(SessionExpired())
    
    user = User.query.get(uid)
    if user is None:
        raise APIException(UserNotFound())
    
    return user





def send_mail(SUBJECT, BODY, TO, attachment = None):

    # Create message container - the correct MIME type is multipart/alternative here!
    MESSAGE = MIMEMultipart('alternative')
    MESSAGE['subject'] = SUBJECT
    MESSAGE['To'] = TO
    MESSAGE['From'] = '"Flashcard no-reply" <core@1nf1n1ty.team>' # Your name
    MESSAGE.preamble = "Your mail reader does not support the format."

    # Record the MIME type text/html.
    HTML_BODY = MIMEText(BODY, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    MESSAGE.attach(HTML_BODY)

    if attachment:
        for data, name in attachment:
            MESSAGE.attach(MIMEApplication(data, Name=name))

    # The actual sending of the e-mail
    server = smtplib.SMTP('smtppro.zoho.in:587')

    server.set_debuglevel(0)

    # Credentials (if needed) for sending the mail
    password = "C!SH1s0urh0m3"

    server.starttls()

    try:
        server.login("core@1nf1n1ty.team",password)
        server.sendmail("core@1nf1n1ty.team", [TO], MESSAGE.as_string())
        server.quit()
        return True
    except:
        return False



    