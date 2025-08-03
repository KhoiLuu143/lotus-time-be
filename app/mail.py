# config/mail.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from dotenv import load_dotenv
import os

load_dotenv()  # Đọc file .env

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_FROM_NAME=os.getenv("MAIL_FROM_NAME"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS") == "True",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS") == "True",
    USE_CREDENTIALS=True,
)

async def send_email(email: EmailStr, token: str):
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    subject = "Xác thực tài khoản của bạn"
    body = f"""
    <h3>Chào bạn!</h3>
    <p>Vui lòng nhấn vào liên kết bên dưới để xác thực email:</p>
    <a href="{verification_link}">{verification_link}</a>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    mail = FastMail(conf)
    await mail.send_message(message)

async def send_reset_email(email: EmailStr, token: str):
    reset_link = f"http://localhost:8000/reset-password?token={token}"
    subject = "Yêu cầu đặt lại mật khẩu"
    body = f"""
    <h3>Chào bạn!</h3>
    <p>Vui lòng nhấn vào liên kết bên dưới để đặt lại mật khẩu:</p>
    <a href="{reset_link}">{reset_link}</a>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype="html"
    )

    mail = FastMail(conf)
    await mail.send_message(message)