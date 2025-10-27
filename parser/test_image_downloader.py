#!/usr/bin/env python3
"""
Тестовый скрипт для проверки скачивания изображений
"""

from image_downloader import ImageDownloader

def test_image_downloader():
    """Тестирует функциональность скачивания изображений"""
    print("🧪 Тестирование ImageDownloader...")
    
    # Создаем экземпляр загрузчика
    downloader = ImageDownloader()
    
    # Тестовые URL'ы
    test_urls = [
        "https://avatars.mds.yandex.net/get-kinopoisk-image/1777765/6ff214c8-e427-4dc2-b447-a1a51743c3ff/280x420",
        "//avatars.mds.yandex.net/get-kinopoisk-image/1704946/5a5a2bdf-6e96-47ed-9675-cb42c1712d3c/280x420",
        "https://yastatic.net/s3/kinopoisk-frontend/common-static/img/projector-logo/placeholder.svg"  # Placeholder
    ]
    
    print(f"\n📥 Тестируем скачивание {len(test_urls)} изображений...")
    
    for i, url in enumerate(test_urls, 1):
        print(f"\n{i}. URL: {url}")
        
        if "placeholder" in url:
            print("   ⏭️ Пропускаем placeholder")
            continue
            
        # Тестируем скачивание постера фильма
        result = downloader.download_film_poster(url, f"test_film_{i}")
        
        if result:
            print(f"   ✅ Скачан: {result}")
            
            # Получаем информацию о файле
            info = downloader.get_image_info(result)
            if info:
                print(f"   📊 Размер: {info['size_mb']} MB")
        else:
            print("   ❌ Ошибка скачивания")
    
    print(f"\n🎉 Тестирование завершено!")
    print(f"📁 Изображения сохранены в папке: {downloader.base_path}")

if __name__ == "__main__":
    test_image_downloader()
