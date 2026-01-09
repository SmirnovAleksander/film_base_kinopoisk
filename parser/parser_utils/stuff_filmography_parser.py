#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для получения фильмографии персоны через GraphQL API Кинопоиска
"""

import requests
import json
from typing import Optional, List
from parser_utils.base_parser import BaseParser


class StuffFilmographyParser(BaseParser):
    """Класс для получения фильмографии персоны через GraphQL API"""

    def __init__(self):
        super().__init__()
        self.graphql_url = "https://graphql.kinopoisk.ru/graphql/"

    def _prepare_session(self):
        """Подготовка сессии с правильными заголовками"""
        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.kinopoisk.ru/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'Service-Id': '25',
            'X-Preferred-Language': 'ru',
            'Priority': 'u=1, i'
        }
        session.headers.update(headers)
        self._load_cookies(session)
        session.headers.update({
            'Content-Type': 'application/json'
        })
        return session

    def fetch_stuff_filmography(self, person_id: int, role_slugs: Optional[List[str]] = None, limit: int = 50):
        """
        Получает фильмографию персоны через GraphQL API с пагинацией

        Args:
            person_id: ID персоны
            role_slugs: Список ролей для фильтрации (например, ["ACTOR"])
            limit: Количество элементов для получения на одной странице
        """
        query = """
        query FilmographyItems($personId: Long!, $roleSlugs: [String], $genre: Int = null, $year: YearsRangeInput = null, $orderBy: FilmographyItemOrderBy = YEAR_DESC, $itemsLimit: Int = 10, $itemsOffset: Int = 0, $participationsLimit: Int = 10, $withUserData: Boolean = false) {
          person(id: $personId) {
            id
            filmographyRelations(roleSlugs: $roleSlugs, limit: $itemsLimit, offset: $itemsOffset, genre: $genre, year: $year, orderBy: $orderBy) {
              items {
                movie {
                  id
                  contentId
                  title {
                    russian
                    original
                    __typename
                  }
                  genres {
                    id
                    name
                    __typename
                  }
                  ...MoviePosterGallery
                  rating {
                    kinopoisk {
                      ...RatingValue
                      __typename
                    }
                    __typename
                  }
                  countries {
                    id
                    name
                    __typename
                  }
                  viewOption {
                    buttonText
                    originalButtonText
                    promotionIcons {
                      avatarsUrl
                      fallbackUrl
                      __typename
                    }
                    isAvailableOnline: isWatchable(filter: {anyDevice: false, anyRegion: false})
                    purchasabilityStatus
                    type
                    rightholderLogoUrlForPoster
                    __typename
                  }
                  ...MovieIsTicketsAvailable
                  ... on Film {
                    productionYear
                    isShortFilm
                    ratingLists {
                      top250 {
                        ...MovieRatingListsItem
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  ... on TvSeries {
                    releaseYears {
                      start
                      end
                      __typename
                    }
                    ratingLists {
                      top250 {
                        ...MovieRatingListsItem
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  ... on MiniSeries {
                    releaseYears {
                      start
                      end
                      __typename
                    }
                    __typename
                  }
                  ... on TvShow {
                    releaseYears {
                      start
                      end
                      __typename
                    }
                    __typename
                  }
                  ... on Video {
                    productionYear
                    isShortFilm
                    __typename
                  }
                  ...FilmographyItemUserData @include(if: $withUserData)
                  __typename
                }
                participations(limit: $participationsLimit) {
                  items {
                    notice
                    role {
                      title {
                        russian
                        english
                        __typename
                      }
                      slug
                      __typename
                    }
                    ... on CastMovieParticipation {
                      name
                      __typename
                    }
                    ... on StaffMovieParticipation {
                      relatedCast {
                        name
                        person {
                          id
                          name
                          originalName
                          url
                          __typename
                        }
                        __typename
                      }
                      __typename
                    }
                    __typename
                  }
                  __typename
                }
                salaries {
                  items {
                    amount
                    currency {
                      symbol
                      __typename
                    }
                    note
                    __typename
                  }
                  __typename
                }
                __typename
              }
              limit
              offset
              total
              __typename
            }
            __typename
          }
        }

        fragment TicketOptionPurchasable on Movie {
          ticketOption {
            purchasable
            __typename
          }
          __typename
        }

        fragment Folder on Folder {
          id
          name
          public
          __typename
        }

        fragment MovieUserFolders on Movie {
          userData {
            userFolders(offset: 0, limit: 20) {
              items {
                ...Folder
                __typename
              }
              __typename
            }
            isFavorite
            __typename
          }
          __typename
        }

        fragment MoviePosterGallery on Movie {
          gallery {
            posters {
              vertical {
                avatarsUrl
                __typename
              }
              __typename
            }
            logos {
              rightholderForPoster {
                avatarsUrl
                __typename
              }
              __typename
            }
            __typename
          }
          __typename
        }

        fragment RatingValue on RatingValue {
          value
          isActive
          count
          __typename
        }

        fragment MovieIsTicketsAvailable on Movie {
          ...TicketOptionPurchasable
          __typename
        }

        fragment MovieRatingListsItem on MovieInList {
          movieListSlug
          position
          __typename
        }

        fragment FilmographyItemUserData on Movie {
          userData {
            watchStatuses {
              notInterested {
                value
                __typename
              }
              watched {
                value
                __typename
              }
              __typename
            }
            voting {
              value
              votedAt
              __typename
            }
            isPlannedToWatch
            __typename
          }
          ...MovieUserFolders
          __typename
        }
        """

        all_filmography_items = []
        offset = 0
        total_items = 0

        session = self._prepare_session()
        url_with_params = f"{self.graphql_url}?operationName=FilmographyItems"

        try:
            while True:
                variables = {
                    "personId": person_id,
                    "roleSlugs": role_slugs,
                    "genre": None,
                    "year": None,
                    "orderBy": "YEAR_DESC",
                    "itemsLimit": limit,
                    "itemsOffset": offset,
                    "participationsLimit": 30,
                    "withUserData": True
                }

                payload = {
                    "operationName": "FilmographyItems",
                    "query": query,
                    "variables": variables
                }

                response = session.post(
                    url_with_params,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                result = response.json()
                
                # Сохраняем сырой ответ для отладки по просьбе пользователя
                import os
                os.makedirs('output', exist_ok=True)
                with open('output/raw_api_debug.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                # print(f"DEBUG: Сырой ответ API сохранен в output/raw_api_debug.json")

                if 'data' in result and 'person' in result['data'] and result['data']['person']:
                    person_data = result['data']['person']
                    filmography_data = (person_data.get('filmographyRelations') or {})
                    total = filmography_data.get('total', 0)
                    items = (filmography_data.get('items') or [])

                    if not items:
                        print("Больше элементов фильмографии нет (пустая страница)")
                        break

                    if total > total_items:
                        total_items = total

                    page_items = 0
                    allowed_roles = ["ACTOR", "DIRECTOR", "PRODUCER", "WRITER"]
                    
                    for item in items:
                        structured_item = self._structure_filmography_item(item, person_id)
                        # Фильтруем по списку разрешенных ролей
                        item_roles = structured_item.get('role_slugs', '').split(',')
                        if structured_item and any(role in item_roles for role in allowed_roles):
                            all_filmography_items.append(structured_item)
                            page_items += 1
                    
                    # print(f"📄 Получено: {len(items)} элементов. Добавлено работ (Актер/Реж/Прод/Сцен): {page_items}. (Всего: {len(all_filmography_items)})")

                    if len(all_filmography_items) >= total:
                        break

                    offset += limit
                else:
                    print("Нет данных в ответе от API или персона не найдена")
                    break

            return all_filmography_items

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            if hasattr(e.response, 'text') and e.response.text:
                print(f"Тело ответа ошибки: {e.response.text}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

    def _structure_filmography_item(self, item: dict, person_id: int) -> dict:
        """
        Структурирует один элемент фильмографии.
        """
        movie = (item.get('movie') or {})
        title = (movie.get('title') or {})
        rating = (movie.get('rating') or {})
        kp_rating = (rating.get('kinopoisk') or {})
        view_option = (movie.get('viewOption') or {})

        structured = {
            'person_id': person_id,
            'movie_id': movie.get('id'),
            'title': title.get('russian'),
            'original_title': title.get('original'),
            'published_year': None, # Будет заполнено ниже
            'genres': [genre.get('name') for genre in (movie.get('genres') or []) if genre.get('name')],
            'countries': [country.get('name') for country in (movie.get('countries') or []) if country.get('name')],
            'poster_url': None, # Будет заполнено ниже
            'rating_kinopoisk': kp_rating.get('value'),
            'rating_kinopoisk_count': kp_rating.get('count'),
            'role_slugs': [], # Будет заполнено ниже
            'release_year_start': None,
            'release_year_end': None,
        }

        # Обработка года производства/выпуска
        if movie.get('__typename') == 'Film':
            structured['published_year'] = movie.get('productionYear')
        elif movie.get('__typename') in ['TvSeries', 'MiniSeries', 'TvShow']:
            release_years = (movie.get('releaseYears') or {})
            
            # releaseYears может быть списком или объектом
            ry_obj = {}
            if isinstance(release_years, list) and release_years:
                ry_obj = (release_years[0] or {})
            elif isinstance(release_years, dict):
                ry_obj = release_years
                
            structured['release_year_start'] = ry_obj.get('start')
            structured['release_year_end'] = ry_obj.get('end')
            # Для сериалов можно взять начальный год как основной год
            structured['published_year'] = ry_obj.get('start')
        elif movie.get('__typename') == 'Video':
            structured['published_year'] = movie.get('productionYear')

        # Обработка постера
        gallery = (movie.get('gallery') or {})
        posters = (gallery.get('posters') or {})
        vertical = (posters.get('vertical') or {})
        
        # vertical может быть списком или объектом
        if isinstance(vertical, list) and vertical:
            vertical_obj = (vertical[0] or {})
        elif isinstance(vertical, dict):
            vertical_obj = vertical
        else:
            vertical_obj = {}
            
        poster_url = vertical_obj.get('avatarsUrl')
        if poster_url:
            structured['poster_url'] = self._normalize_url(poster_url)

        # Обработка ролей
        participations_data = (item.get('participations') or {})
        participations = (participations_data.get('items') or [])
        for p in participations:
            if not p: continue
            role = (p.get('role') or {})
            if role.get('slug'):
                structured['role_slugs'].append(role.get('slug'))
        
        # Удаляем дубликаты и приводим к строке
        structured['role_slugs'] = ','.join(sorted(list(set(structured['role_slugs']))))
        structured['genres'] = ','.join(sorted(list(set(structured['genres']))))
        structured['countries'] = ','.join(sorted(list(set(structured['countries']))))

        return structured


def main():
    """Основная функция"""
    fetcher = StuffFilmographyParser()

    # Пример использования
    person_id = 797  # Пример ID актера
    limit = 50

    print(f"Получение фильмографии для персоны ID: {person_id}")
    filmography = fetcher.fetch_stuff_filmography(person_id, role_slugs=["ACTOR"], limit=limit)

    if filmography:
        print(f"Всего фильмов найдено: {len(filmography)}")
        # Сохраняем в JSON для проверки
        fetcher.save_to_json(filmography, f"output/filmography_{person_id}.json")
    else:
        print("Не удалось получить фильмографию.")


if __name__ == "__main__":
    main()