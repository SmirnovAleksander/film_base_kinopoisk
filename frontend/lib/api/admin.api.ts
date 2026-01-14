import { AdminFilmsAPI } from './admin/films';
import { AdminStuffAPI } from './admin/stuff';
import { AdminGenresAPI } from './admin/genres';
import { AdminCountriesAPI } from './admin/countries';
import { AdminMediaAPI } from './admin/media';
import { AdminUsersAPI } from './admin/users';
import { AdminFilmDetailsAPI } from './admin/film-details';
import { AdminFilmRelationsAPI } from './admin/film-relations';

export class AdminAPI {
  // фильмы
  static createFilm = AdminFilmsAPI.createFilm;
  static getAllFilms = AdminFilmsAPI.getAllFilms;
  static getFilmById = AdminFilmsAPI.getFilmById;
  static updateFilm = AdminFilmsAPI.updateFilm;
  static deleteFilm = AdminFilmsAPI.deleteFilm;

  // участники
  static createStuff = AdminStuffAPI.createStuff;
  static getAllStuff = AdminStuffAPI.getAllStuff;
  static getAllStuffAll = AdminStuffAPI.getAllStuffAll;
  static getStuffById = AdminStuffAPI.getStuffById;
  static updateStuff = AdminStuffAPI.updateStuff;
  static deleteStuff = AdminStuffAPI.deleteStuff;

  // жанры
  static createGenre = AdminGenresAPI.createGenre;
  static getAllGenres = AdminGenresAPI.getAllGenres;
  static getGenreById = AdminGenresAPI.getGenreById;
  static updateGenre = AdminGenresAPI.updateGenre;
  static deleteGenre = AdminGenresAPI.deleteGenre;

  // страны
  static createCountry = AdminCountriesAPI.createCountry;
  static getAllCountries = AdminCountriesAPI.getAllCountries;
  static getCountryById = AdminCountriesAPI.getCountryById;
  static updateCountry = AdminCountriesAPI.updateCountry;
  static deleteCountry = AdminCountriesAPI.deleteCountry;

  // медиа
  static createMedia = AdminMediaAPI.createMedia;
  static getAllMedia = AdminMediaAPI.getAllMedia;
  static getMediaById = AdminMediaAPI.getMediaById;
  static updateMedia = AdminMediaAPI.updateMedia;
  static deleteMedia = AdminMediaAPI.deleteMedia;

  // пользователи
  static createUser = AdminUsersAPI.createUser;
  static getAllUsers = AdminUsersAPI.getAllUsers;
  static getUserById = AdminUsersAPI.getUserById;
  static updateUser = AdminUsersAPI.updateUser;
  static deleteUser = AdminUsersAPI.deleteUser;

  // дополнительные детали
  static createSimilarFilm = AdminFilmDetailsAPI.createSimilarFilm;
  static getAllSimilarFilms = AdminFilmDetailsAPI.getAllSimilarFilms;
  static getSimilarFilmById = AdminFilmDetailsAPI.getSimilarFilmById;
  static updateSimilarFilm = AdminFilmDetailsAPI.updateSimilarFilm;
  static deleteSimilarFilm = AdminFilmDetailsAPI.deleteSimilarFilm;

  static createFilmStill = AdminFilmDetailsAPI.createFilmStill;
  static getAllFilmStills = AdminFilmDetailsAPI.getAllFilmStills;
  static getFilmStillById = AdminFilmDetailsAPI.getFilmStillById;
  static updateFilmStill = AdminFilmDetailsAPI.updateFilmStill;
  static deleteFilmStill = AdminFilmDetailsAPI.deleteFilmStill;

  static createFilmWatchProvider = AdminFilmDetailsAPI.createFilmWatchProvider;
  static getAllFilmWatchProviders = AdminFilmDetailsAPI.getAllFilmWatchProviders;
  static getFilmWatchProviderById = AdminFilmDetailsAPI.getFilmWatchProviderById;
  static updateFilmWatchProvider = AdminFilmDetailsAPI.updateFilmWatchProvider;
  static deleteFilmWatchProvider = AdminFilmDetailsAPI.deleteFilmWatchProvider;

  // связь
  static createFilmGenre = AdminFilmRelationsAPI.createFilmGenre;
  static getAllFilmGenres = AdminFilmRelationsAPI.getAllFilmGenres;
  static getFilmGenreById = AdminFilmRelationsAPI.getFilmGenreById;
  static deleteFilmGenre = AdminFilmRelationsAPI.deleteFilmGenre;

  static createFilmCountry = AdminFilmRelationsAPI.createFilmCountry;
  static getAllFilmCountries = AdminFilmRelationsAPI.getAllFilmCountries;
  static getFilmCountryById = AdminFilmRelationsAPI.getFilmCountryById;
  static deleteFilmCountry = AdminFilmRelationsAPI.deleteFilmCountry;

  static createFilmStuff = AdminFilmRelationsAPI.createFilmStuff;
  static getAllFilmStuff = AdminFilmRelationsAPI.getAllFilmStuff;
  static getFilmStuffById = AdminFilmRelationsAPI.getFilmStuffById;
  static updateFilmStuff = AdminFilmRelationsAPI.updateFilmStuff;
  static deleteFilmStuff = AdminFilmRelationsAPI.deleteFilmStuff;
}