from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib


async def send_email(
        recipient: str,
        subject: str,
        plain_content: str,
        html_content: str = "",
):
    admin_email = "aleksander50.500@gmail.com"
    message = MIMEMultipart("alternative")
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject

    plain_text_message = MIMEText(
        plain_content,
        "plain",
        "utf-8"
    )
    message.attach(plain_text_message)

    if html_content:
        html_message = MIMEText(
            html_content,
            "html",
            "utf-8"
        )
        message.attach(html_message)

    # await aiosmtplib.send(
    #     message,
    #     hostname="0.0.0.0",
    #     port=1025
    # )

    # Временное решение: логируем email вместо отправки
    print(f"\n📧 EMAIL WOULD BE SENT:")
    print(f"To: {recipient}")
    print(f"Subject: {subject}")
    print(f"Content: {plain_content}")
    if html_content:
        print(f"HTML Content: {html_content}")
    print("-" * 50)