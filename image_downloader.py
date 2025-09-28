import os
import requests
import hashlib
from urllib.parse import urlparse
from pathlib import Path

class ImageDownloader:
    """Класс для скачивания и сохранения изображений"""
    
    def __init__(self, base_path="images"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Создаем папки для разных типов изображений
        (self.base_path / "films").mkdir(exist_ok=True)
        (self.base_path / "actors").mkdir(exist_ok=True)
        (self.base_path / "temp").mkdir(exist_ok=True)
    
    def download_image(self, url, image_type, filename=None):
        """
        Скачивает изображение и сохраняет в локальную файловую систему
        
        Args:
            url (str): URL изображения
            image_type (str): Тип изображения ('films' или 'actors')
            filename (str, optional): Имя файла. Если не указано, генерируется автоматически
        
        Returns:
            str: Путь к сохраненному файлу или None при ошибке
        """
        if not url or url.startswith('https://yastatic.net'):
            # Пропускаем placeholder изображения
            return None
            
        try:
            # Нормализуем URL
            if url.startswith('//'):
                url = 'https:' + url
            elif not url.startswith('http'):
                url = 'https://' + url
            
            # Генерируем имя файла если не указано
            if not filename:
                # Извлекаем расширение из URL
                parsed_url = urlparse(url)
                path = parsed_url.path
                ext = os.path.splitext(path)[1] or '.jpg'
                
                # Генерируем уникальное имя на основе URL
                url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
                filename = f"{url_hash}{ext}"
            
            # Определяем путь для сохранения
            save_path = self.base_path / image_type / filename
            
            # Скачиваем изображение
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Сохраняем файл
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            # Возвращаем относительный путь
            return f"images/{image_type}/{filename}"
            
        except Exception as e:
            print(f"❌ Ошибка скачивания изображения {url}: {e}")
            return None
    
    def download_film_poster(self, url, film_id):
        """Скачивает постер фильма"""
        if not url:
            return None
        
        # Генерируем имя файла на основе ID фильма
        filename = f"film_{film_id}.jpg"
        return self.download_image(url, "films", filename)
    
    def download_actor_photo(self, url, actor_id):
        """Скачивает фото актера"""
        if not url:
            return None
        
        # Генерируем имя файла на основе ID актера
        filename = f"actor_{actor_id}.jpg"
        return self.download_image(url, "actors", filename)
    
    def cleanup_temp_files(self):
        """Очищает временные файлы"""
        temp_dir = self.base_path / "temp"
        if temp_dir.exists():
            for file in temp_dir.iterdir():
                if file.is_file():
                    file.unlink()
    
    def get_image_info(self, image_path):
        """Получает информацию о сохраненном изображении"""
        if not image_path or not os.path.exists(image_path):
            return None
        
        file_size = os.path.getsize(image_path)
        return {
            'path': image_path,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'exists': True
        }
