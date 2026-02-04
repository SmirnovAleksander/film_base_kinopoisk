[baseline-browser-mapping] The data in this module is over two months old.  To ensure accurate Baseline data, please update: `npm i baseline-browser-mapping@latest -D`

D:\study_projects\film_base_kinopoisk\frontend\app\admin\page.tsx
  15:11  error    An interface declaring no members is equivalent to its supertype                                             @typescript-eslint/no-empty-object-type
  51:6   warning  React Hook useEffect has a missing dependency: 'loadData'. Either include it or remove the dependency array  react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\app\bookmarks\page.tsx
  14:5  warning  'isLoadingBookmarks' is assigned a value but never used  @typescript-eslint/no-unused-vars

D:\study_projects\film_base_kinopoisk\frontend\app\films\[id]\page.tsx
   92:6   warning  React Hook useEffect has missing dependencies: 'fetchFilmComments', 'fetchFilmDetails', 'loadFilmStills', 'loadFilmStuff', 'loadRecommendedFilms', 'loadSimilarFilms', and 'loadWatchProviders'. Either include them or remove the dependency array  react-hooks/exhaustive-deps
  156:18  warning  'error' is defined but never used                                                                                                                                                                                              
                      @typescript-eslint/no-unused-vars
  345:19  error    `"` can be escaped with `&quot;`, `&ldquo;`, `&#34;`, `&rdquo;`                                                                                                                                                                
                      react/no-unescaped-entities
  345:41  error    `"` can be escaped with `&quot;`, `&ldquo;`, `&#34;`, `&rdquo;`                                                                                                                                                                
                      react/no-unescaped-entities

D:\study_projects\film_base_kinopoisk\frontend\app\films\page.tsx
   3:21  warning  'useState' is defined but never used                                                                   
                                           @typescript-eslint/no-unused-vars
  77:6   warning  React Hook useEffect has missing dependencies: 'filterFilms', 'handleSearch', and 'pageSize'. Either include them or remove the dependency array  react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\app\history\page.tsx
  16:5   error    Error: Calling setState synchronously within an effect can trigger cascading renders

Effects are intended to synchronize state between React and external systems such as manually updating the DOM, state management libraries, or other platform APIs. In general, the body of an effect should do one or both of the following:     
* Update external systems with the latest state from React.
* Subscribe for updates from some external system, calling setState in a callback function when external state changes.  

Calling setState synchronously within an effect body causes cascading renders that can hurt performance, and is not recommended. (https://react.dev/learn/you-might-not-need-an-effect).

D:\study_projects\film_base_kinopoisk\frontend\app\history\page.tsx:16:5
  14 |
  15 |   useEffect(() => {
> 16 |     setMounted(true);
     |     ^^^^^^^^^^ Avoid calling setState() directly within an effect
  17 |   }, []);
  18 |
  19 |   const formatDate = (dateString: string) => {  react-hooks/set-state-in-effect
  69:23  warning  Using `<img>` could result in slower LCP and higher bandwidth. Consider using `<Image />` from `next/image` or a custom image loader to automatically optimize images. This may incur additional usage or cost from your provider. See: https://nextjs.org/docs/messages/no-img-element                                                                  
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                             @next/next/no-img-element

D:\study_projects\film_base_kinopoisk\frontend\app\posters\[id]\page.tsx
   8:3   warning  'Maximize2' is defined but never used                                                                  
            @typescript-eslint/no-unused-vars
  13:41  warning  'CardTitle' is defined but never used                                                                  
            @typescript-eslint/no-unused-vars
  51:9   warning  'totalCount' is assigned a value but never used                                                        
            @typescript-eslint/no-unused-vars
  59:6   warning  React Hook useEffect has a missing dependency: 'loadFilmStills'. Either include it or remove the dependency array  react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\app\profile\page.tsx
   13:17  warning  'updateUser' is assigned a value but never used                                                       
                                                                                                                         
                                                          @typescript-eslint/no-unused-vars
   13:29  warning  'isLoading' is assigned a value but never used                                                        
                                                                                                                         
                                                          @typescript-eslint/no-unused-vars
   26:6   warning  React Hook useEffect has missing dependencies: 'fetchBookmarks' and 'fetchUserRatings'. Either include them or remove the dependency array                                                                                     
                                                          react-hooks/exhaustive-deps
  159:25  warning  Using `<img>` could result in slower LCP and higher bandwidth. Consider using `<Image />` from `next/image` or a custom image loader to automatically optimize images. This may incur additional usage or cost from your provider. See: https://nextjs.org/docs/messages/no-img-element  @next/next/no-img-element

D:\study_projects\film_base_kinopoisk\frontend\app\stuff\[id]\page.tsx
  32:6  warning  React Hook useEffect has a missing dependency: 'loadStuffDetails'. Either include it or remove the dependency array  react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\app\verify-email\page.tsx
  27:6  warning  React Hook useEffect has a missing dependency: 'handleVerify'. Either include it or remove the dependency array  react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\components\admin\AdminSidebar.tsx
   9:3  warning  'Newspaper' is defined but never used  @typescript-eslint/no-unused-vars
  11:3  warning  'Home' is defined but never used       @typescript-eslint/no-unused-vars

D:\study_projects\film_base_kinopoisk\frontend\components\admin\NavMain.tsx
  22:5  error  Error: This value cannot be modified

Modifying a variable defined outside a component or hook is not allowed. Consider using an effect.

D:\study_projects\film_base_kinopoisk\frontend\components\admin\NavMain.tsx:22:5
  20 | export function NavMain({ items, activeTab }: NavMainProps) {
  21 |   const handleClick = (url: string) => {
> 22 |     window.location.hash = url
     |     ^^^^^^^^^^^^^^^ value cannot be modified
  23 |   }
  24 |
  25 |   return (  react-hooks/immutability

D:\study_projects\film_base_kinopoisk\frontend\components\admin\forms\FilmForm.tsx
   11:3  warning  'SimilarFilmUpdate' is defined but never used                                                          
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                          @typescript-eslint/no-unused-vars
   14:3  warning  'FilmStillUpdate' is defined but never used                                                            
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                          @typescript-eslint/no-unused-vars
   17:3  warning  'FilmWatchProviderUpdate' is defined but never used                                                    
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                          @typescript-eslint/no-unused-vars
   24:3  warning  'FilmStuffUpdate' is defined but never used                                                            
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                          @typescript-eslint/no-unused-vars
  173:7  error    Error: Cannot access variable before it is declared

`loadRelatedData` is accessed before it is declared, which prevents the earlier access from updating when this value changes over time.

D:\study_projects\film_base_kinopoisk\frontend\components\admin\forms\FilmForm.tsx:173:7
  171 |   useEffect(() => {
  172 |     if (film?.id) {
> 173 |       loadRelatedData();
      |       ^^^^^^^^^^^^^^^ `loadRelatedData` accessed before it is declared
  174 |       loadReferenceData();
  175 |     }
  176 |   }, [film?.id]);

D:\study_projects\film_base_kinopoisk\frontend\components\admin\forms\FilmForm.tsx:178:3
  176 |   }, [film?.id]);
  177 |
> 178 |   const loadRelatedData = async () => {
      |   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 179 |     if (!film?.id) return;
      | ^^^^^^^^^^^^^^^^^^^^^^^^^^
> 180 |
      …
      | ^^^^^^^^^^^^^^^^^^^^^^^^^^
> 199 |     }
      | ^^^^^^^^^^^^^^^^^^^^^^^^^^
> 200 |   };
      | ^^^^^ `loadRelatedData` is declared here
  201 |
  202 |   const loadReferenceData = async () => {
  203 |     try {  react-hooks/immutability
  174:7  error    Error: Cannot access variable before it is declared

`loadReferenceData` is accessed before it is declared, which prevents the earlier access from updating when this value changes over time.

D:\study_projects\film_base_kinopoisk\frontend\components\admin\forms\FilmForm.tsx:174:7
  172 |     if (film?.id) {
  173 |       loadRelatedData();
> 174 |       loadReferenceData();
      |       ^^^^^^^^^^^^^^^^^ `loadReferenceData` accessed before it is declared
  175 |     }
  176 |   }, [film?.id]);
  177 |

D:\study_projects\film_base_kinopoisk\frontend\components\admin\forms\FilmForm.tsx:202:3
  200 |   };
  201 |
> 202 |   const loadReferenceData = async () => {
      |   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 203 |     try {
      | ^^^^^^^^^
> 204 |       const [genresData, countriesData, stuffData] = await Promise.all([
      …
      | ^^^^^^^^^
> 215 |     }
      | ^^^^^^^^^
> 216 |   };
      | ^^^^^ `loadReferenceData` is declared here
  217 |
  218 |   const handleSubmit = (e: React.FormEvent) => {
  219 |     e.preventDefault();  react-hooks/immutability
  176:6  warning  React Hook useEffect has a missing dependency: 'loadRelatedData'. Either include it or remove the dependency array                                                                                                              
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                          react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\components\carousel\FilmStillsCarousel.tsx
   64:5  error    Error: Calling setState synchronously within an effect can trigger cascading renders

Effects are intended to synchronize state between React and external systems such as manually updating the DOM, state management libraries, or other platform APIs. In general, the body of an effect should do one or both of the following:     
* Update external systems with the latest state from React.
* Subscribe for updates from some external system, calling setState in a callback function when external state changes.  

Calling setState synchronously within an effect body causes cascading renders that can hurt performance, and is not recommended. (https://react.dev/learn/you-might-not-need-an-effect).

D:\study_projects\film_base_kinopoisk\frontend\components\carousel\FilmStillsCarousel.tsx:64:5
  62 |     if (!emblaApi) return;
  63 |
> 64 |     onInit(emblaApi);
     |     ^^^^^^ Avoid calling setState() directly within an effect
  65 |     onSelect(emblaApi);
  66 |
  67 |     emblaApi.on('reInit', onInit);  react-hooks/set-state-in-effect
  125:6  warning  React Hook useEffect has a missing dependency: 'setTweenFactor'. Either include it or remove the dependency array                                                                                                               
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                        react-hooks/exhaustive-deps

D:\study_projects\film_base_kinopoisk\frontend\components\film\FilmCard.tsx
  228:8  error  Error: Cannot create components during render

Components created during render will reset their state each time they are created. Declare components outside of render.

D:\study_projects\film_base_kinopoisk\frontend\components\film\FilmCard.tsx:228:8
  226 |   return (
  227 |     <Card className={`group overflow-hidden transition-all duration-200 pt-0 hover:shadow-lg ${className}`}>     
> 228 |       <LinkWrapper>
      |        ^^^^^^^^^^^ This component is created during render
  229 |         {cardContent}
  230 |       </LinkWrapper>
  231 |     </Card>

D:\study_projects\film_base_kinopoisk\frontend\components\film\FilmCard.tsx:82:7
  80 |
  81 |   const LinkWrapper = isExternal && externalUrl
> 82 |     ? ({ children }: { children: React.ReactNode }) => (
     |       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 83 |       <a href={externalUrl} target="_blank" rel="noopener noreferrer" className="block">
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 84 |         {children}
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 85 |       </a>
     | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
> 86 |     )
     | ^^^^^^ The component is created during render here
  87 |     : ({ children }: { children: React.ReactNode }) => (
  88 |       <Link href={ROUTES.FILM_DETAILS(film.id)} className="block">
  89 |         {children}  react-hooks/static-components

D:\study_projects\film_base_kinopoisk\frontend\components\film\FilmsFilters.tsx
  37:3  warning  'totalCount' is defined but never used                                                                  
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                             @typescript-eslint/no-unused-vars
  39:3  warning  'isSearching' is defined but never used                                                                 
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                                                         
                                                                                             @typescript-eslint/no-unused-vars
  55:5  error    Error: Calling setState synchronously within an effect can trigger cascading renders

Effects are intended to synchronize state between React and external systems such as manually updating the DOM, state management libraries, or other platform APIs. In general, the body of an effect should do one or both of the following:     
* Update external systems with the latest state from React.
* Subscribe for updates from some external system, calling setState in a callback function when external state changes.  

Calling setState synchronously within an effect body causes cascading renders that can hurt performance, and is not recommended. (https://react.dev/learn/you-might-not-need-an-effect).

D:\study_projects\film_base_kinopoisk\frontend\components\film\FilmsFilters.tsx:55:5
  53 |
  54 |   useEffect(() => {
> 55 |     setLocalSearchQuery(searchQuery);
     |     ^^^^^^^^^^^^^^^^^^^ Avoid calling setState() directly within an effect
  56 |     setLocalFilters(filters);
  57 |
  58 |     if (filters.start_year || filters.end_year) {  react-hooks/set-state-in-effect

D:\study_projects\film_base_kinopoisk\frontend\components\layout\header.tsx
  18:12  warning  'ImageIcon' is defined but never used       @typescript-eslint/no-unused-vars
  49:11  warning  'theme' is assigned a value but never used  @typescript-eslint/no-unused-vars

D:\study_projects\film_base_kinopoisk\frontend\components\ui\sidebar.tsx
  611:26  error  Error: Cannot call impure function during render

`Math.random` is an impure function. Calling an impure function can produce unstable results that update unpredictably when the component happens to re-render. (https://react.dev/reference/rules/components-and-hooks-must-be-pure#components-and-hooks-must-be-idempotent).

D:\study_projects\film_base_kinopoisk\frontend\components\ui\sidebar.tsx:611:26
  609 |   // Random width between 50 to 90%.
  610 |   const width = React.useMemo(() => {
> 611 |     return `${Math.floor(Math.random() * 40) + 50}%`
      |                          ^^^^^^^^^^^^^ Cannot call impure function
  612 |   }, [])
  613 |
  614 |   return (  react-hooks/purity

D:\study_projects\film_base_kinopoisk\frontend\lib\api\client.api.ts
  70:18  warning  'refreshError' is defined but never used  @typescript-eslint/no-unused-vars

D:\study_projects\film_base_kinopoisk\frontend\lib\types\comments.types.ts
  11:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type

D:\study_projects\film_base_kinopoisk\frontend\lib\types\country.types.ts
  7:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type 
  8:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type 

D:\study_projects\film_base_kinopoisk\frontend\lib\types\film_details.types.ts
  24:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type
  85:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type

D:\study_projects\film_base_kinopoisk\frontend\lib\types\film_relations.types.ts
  25:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type

D:\study_projects\film_base_kinopoisk\frontend\lib\types\genre.types.ts
  7:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type 
  8:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type 

D:\study_projects\film_base_kinopoisk\frontend\lib\types\stuff.types.ts
  21:18  error  An interface declaring no members is equivalent to its supertype  @typescript-eslint/no-empty-object-type

D:\study_projects\film_base_kinopoisk\frontend\store\auth.store.ts
  36:31  warning  'token_type' is assigned a value but never used  @typescript-eslint/no-unused-vars

D:\study_projects\film_base_kinopoisk\frontend\store\user.store.ts
  182:14  warning  'error' is defined but never used  @typescript-eslint/no-unused-vars

✖ 52 problems (20 errors, 32 warnings)