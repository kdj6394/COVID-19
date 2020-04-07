# 1. __The Lists of Data Table__
1. __Case Data__
    * __Case__: Data of COVID-1 infection cases in South Korea
2. __Patient Data__
    * __PatientInfo__: Epidemiological data of COVID-19 patients in South Korea
    * __PatientRoute__: Route data of COVID-19 patients in South Korea
3. __Time Series Data__
    * __Time__: Time series data of COVID-19 status in South Korea
    * __TimeAge__: Time series data of COVID-19 status in terms of the age in South Korea
    * __TimeGender__: Time series data of COVID-19 status in terms of gender in South Korea
    * __TimeProvince__: Time series data of COVID-19 status in terms of the Province in South Korea
4. __Additional Data__
    * __Region__: Location and statistical data of the regions in South Korea
    * __Weather__: Data of the weather in the regions of South Korea
    * __SearchTrend__: Trend data of the keywords searched in NAVER which is one of the largest portals in South Korea
# 2. __The Structure of our Dataset__
* What color means is that they have similar properties.
* If a line is connected between columns, it means that the values of the columns are partially shared.
* The dotted lines mean weak relevance
![이미지](https://user-images.githubusercontent.com/50820635/76959778-a4718700-695d-11ea-864c-379c2c9b97a6.PNG)

# 3. __The Detailed Description of each Data Table__
## ___Before the Start___
* We make a structured dataset based on the report materials of KCDC and local governments.
* In Korea, we use the terms named '-do', '-si', '-gun' and '-gu',
* The meaning of them are explained below.

## __Levels of administrative__ divisions in South Korea
__Upper Level (Provincial-level divisions)__
* __Special City__: Seoul
* __Metropolitan City__: Busan / Daegu / Daejeon / Gwangju / Incheon / Ulsan
* __Province(-do)__: Gyeonggi-do / Gangwon-do / Chungcheongbuk-do / Chungcheongnam-do / Jeollabuk-do / Jeollanam-do / Gyeongsangbuk-do / Gyeongsangnam-do

__Lower Level (Municipal-level divisions)__
* __City(-si)__ [List of cities in South Korea](https://en.wikipedia.org/wiki/List_of_cities_in_South_Korea)
* __Country(-gun)__ [List of counties of South Korea](https://en.wikipedia.org/wiki/List_of_counties_of_South_Korea)
* __District(-gu)__ [List of districts in South Korea](https://en.wikipedia.org/wiki/List_of_districts_in_South_Korea)

![이미지](https://www.googleapis.com/download/storage/v1/b/kaggle-user-content/o/inbox%2F2815958%2F1c50702025f44b0c1ce92460bd2ea3f9%2Fus_hi_30-1.jpg?generation=1582819435038273&alt=media)


Sources

<http://nationalatlas.ngii.go.kr/pages/page_1266.php>
<https://en.wikipedia.org/wiki/Administrative_divisions_of_South_Korea>

