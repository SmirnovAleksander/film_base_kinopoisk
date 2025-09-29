#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест отправки красивых писем для Film Base API
"""

import asyncio
from backend.utils.mailer import send_verification_email, send_password_reset_email


async def test_verification_email():
    """Тестирует красивое письмо подтверждения регистрации"""
    print("🔐 Тестирование красивого письма подтверждения регистрации...")
    
    # Тестовые данные
    email = "andrewdurev506@gmail.com"  # Замени на свою почту для тестирования
    token = "test_verification_token_12345"
    username = "TestUser"
    
    try:
        result = await send_verification_email(email, token, username)
        if result:
            print("✅ Красивое письмо подтверждения отправлено!")
            print(f"📧 Письмо отправлено на: {email}")
            print(f"🔗 Токен: {token}")
        else:
            print("❌ Ошибка при отправке письма подтверждения")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def test_password_reset_email():
    """Тестирует красивое письмо сброса пароля"""
    print("\n🔑 Тестирование красивого письма сброса пароля...")
    
    # Тестовые данные
    email = "andrewdurev506@gmail.com"  # Замени на свою почту для тестирования
    token = "test_reset_token_67890"
    username = "TestUser"
    
    try:
        result = await send_password_reset_email(email, token, username)
        if result:
            print("✅ Красивое письмо сброса пароля отправлено!")
            print(f"📧 Письмо отправлено на: {email}")
            print(f"🔗 Токен: {token}")
        else:
            print("❌ Ошибка при отправке письма сброса пароля")
    except Exception as e:
        print(f"❌ Ошибка: {e}")


async def main():
    """Главная функция тестирования красивых писем"""
    print("🚀 Тестирование красивых писем для Film Base API")
    print("=" * 60)
    
    # Проверяем конфигурацию
    try:
        from config import MAIL_CONFIG
        print(f"📧 Настроенная почта: {MAIL_CONFIG['MAIL_USERNAME']}")
        print(f"🖥️ SMTP сервер: {MAIL_CONFIG['MAIL_SERVER']}:{MAIL_CONFIG['MAIL_PORT']}")
        print(f"📤 От кого отправлять: {MAIL_CONFIG['MAIL_FROM']}")
        
        if MAIL_CONFIG['MAIL_USERNAME'] == "your_email@gmail.com":
            print("⚠️ Внимание: Используются тестовые настройки почты!")
            print("📝 Обновите config.py с реальными данными для отправки писем")
    except ImportError:
        print("❌ Не удалось импортировать конфигурацию почты")
        return
    
    print("\n" + "=" * 60)
    
    # Запускаем тесты красивых писем
    await test_verification_email()
    await test_password_reset_email()
    
    print("\n" + "=" * 60)
    print("🎉 Тестирование красивых писем завершено!")
    print("\n📋 Что нового:")
    print("✨ Красивые HTML письма с градиентами и анимациями")
    print("🎨 Адаптивный дизайн для мобильных устройств")
    print("🔗 Готовые ссылки для подтверждения и сброса пароля")
    print("📱 Эмодзи и современный дизайн")
    print("\n🚀 Следующие шаги:")
    print("1. Протестируйте регистрацию через API")
    print("2. Проверьте получение красивых писем")
    print("3. Настройте фронтенд для обработки ссылок")


if __name__ == "__main__":
    asyncio.run(main())
