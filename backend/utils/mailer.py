import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from fastapi_mail.errors import ConnectionErrors


# Для простоты берём настройки из env через ConnectionConfig по-умолчанию
# Рекомендуется вынести в config.py/Pydantic Settings
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "no-reply@example.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", "587")),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.mailtrap.io"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "true").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "false").lower() == "true",
    USE_CREDENTIALS=os.getenv("MAIL_USE_CREDENTIALS", "true").lower() == "true",
)


async def send_email(subject: str, recipients: list[str], html: str) -> bool:
    # Fallback: если не настроены креды, выводим письмо в консоль и не падаем
    if not conf.MAIL_USERNAME or not conf.MAIL_PASSWORD:
        print("[MAIL:FALLBACK]", {"subject": subject, "recipients": recipients, "html": html})
        return True

    message = MessageSchema(subject=subject, recipients=recipients, body=html, subtype="html")
    fm = FastMail(conf)
    try:
        await fm.send_message(message)
        return True
    except ConnectionErrors as e:
        print(f"[MAIL:ERROR] SMTP connection error: {e}")
        return False
    except Exception as e:
        print(f"[MAIL:ERROR] Unexpected: {e}")
        return False


