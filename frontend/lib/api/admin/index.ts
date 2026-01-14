import { AdminFilmsAPI } from './films.admin.api';
import { AdminSeriesAPI } from './series.admin.api';
import { AdminStuffAPI } from './stuff.admin.api';
import { AdminGenresAPI } from './genres.admin.api';
import { AdminCountriesAPI } from './countries.admin.api';
import { AdminMediaAPI } from './media.admin.api';
import { AdminUsersAPI } from './users.admin.api';
import { AdminContentDetailsAPI } from './content-details.admin.api';

export * from './films.admin.api';
export * from './series.admin.api';
export * from './stuff.admin.api';
export * from './genres.admin.api';
export * from './countries.admin.api';
export * from './media.admin.api';
export * from './users.admin.api';
export * from './content-details.admin.api';

export class AdminAPI {
    // Films
    static createFilm = AdminFilmsAPI.createFilm;
    static getAllFilms = AdminFilmsAPI.getAllFilms;
    static getFilmById = AdminFilmsAPI.getFilmById;
    static updateFilm = AdminFilmsAPI.updateFilm;
    static deleteFilm = AdminFilmsAPI.deleteFilm;

    // Series
    static createSeries = AdminSeriesAPI.createSeries;
    static getAllSeries = AdminSeriesAPI.getAllSeries;
    static getSeriesById = AdminSeriesAPI.getSeriesById;
    static updateSeries = AdminSeriesAPI.updateSeries;
    static deleteSeries = AdminSeriesAPI.deleteSeries;

    // Stuff
    static createStuff = AdminStuffAPI.createStuff;
    static getAllStuff = AdminStuffAPI.getAllStuff;
    static getStuffById = AdminStuffAPI.getStuffById;
    static updateStuff = AdminStuffAPI.updateStuff;
    static deleteStuff = AdminStuffAPI.deleteStuff;

    // Genres
    static createGenre = AdminGenresAPI.createGenre;
    static getAllGenres = AdminGenresAPI.getAllGenres;
    static getGenreById = AdminGenresAPI.getGenreById;
    static updateGenre = AdminGenresAPI.updateGenre;
    static deleteGenre = AdminGenresAPI.deleteGenre;

    // Countries
    static createCountry = AdminCountriesAPI.createCountry;
    static getAllCountries = AdminCountriesAPI.getAllCountries;
    static getCountryById = AdminCountriesAPI.getCountryById;
    static updateCountry = AdminCountriesAPI.updateCountry;
    static deleteCountry = AdminCountriesAPI.deleteCountry;

    // Media
    static createMedia = AdminMediaAPI.createMedia;
    static getAllMedia = AdminMediaAPI.getAllMedia;
    static getMediaById = AdminMediaAPI.getMediaById;
    static updateMedia = AdminMediaAPI.updateMedia;
    static deleteMedia = AdminMediaAPI.deleteMedia;

    // Users
    static createUser = AdminUsersAPI.createUser;
    static getAllUsers = AdminUsersAPI.getAllUsers;
    static getUserById = AdminUsersAPI.getUserById;
    static updateUser = AdminUsersAPI.updateUser;
    static deleteUser = AdminUsersAPI.deleteUser;

    // Content Details
    static createContentImage = AdminContentDetailsAPI.createContentImage;
    static getAllContentImages = AdminContentDetailsAPI.getAllContentImages;
    static getContentImageById = AdminContentDetailsAPI.getContentImageById;
    static deleteContentImage = AdminContentDetailsAPI.deleteContentImage;

    static createContentWatchProvider = AdminContentDetailsAPI.createContentWatchProvider;
    static getAllContentWatchProviders = AdminContentDetailsAPI.getAllContentWatchProviders;
    static getContentWatchProviderById = AdminContentDetailsAPI.getContentWatchProviderById;
    static deleteContentWatchProvider = AdminContentDetailsAPI.deleteContentWatchProvider;

    static createSimilarContent = AdminContentDetailsAPI.createSimilarContent;
    static getAllSimilarContent = AdminContentDetailsAPI.getAllSimilarContent;
    static getSimilarContentById = AdminContentDetailsAPI.getSimilarContentById;
    static deleteSimilarContent = AdminContentDetailsAPI.deleteSimilarContent;

    static createContentGenre = AdminContentDetailsAPI.createContentGenre;
    static getAllContentGenres = AdminContentDetailsAPI.getAllContentGenres;
    static getContentGenreById = AdminContentDetailsAPI.getContentGenreById;
    static deleteContentGenre = AdminContentDetailsAPI.deleteContentGenre;

    static createContentCountry = AdminContentDetailsAPI.createContentCountry;
    static getAllContentCountries = AdminContentDetailsAPI.getAllContentCountries;
    static getContentCountryById = AdminContentDetailsAPI.getContentCountryById;
    static deleteContentCountry = AdminContentDetailsAPI.deleteContentCountry;

    static createContentStuff = AdminContentDetailsAPI.createContentStuff;
    static getAllContentStuff = AdminContentDetailsAPI.getAllContentStuff;
    static getContentStuffById = AdminContentDetailsAPI.getContentStuffById;
    static deleteContentStuff = AdminContentDetailsAPI.deleteContentStuff;
}
