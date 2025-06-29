# CLIWOC visualization

## What is CLIWOC
CLImatological Database for the World's OCeans 1750-1850 (CLIWOC) was an European Union funded project (2001-2003). The project was leaded by Universidad Complutense de Madrid in partnership with University of Sunderland, University of East Anglia, Royal Netherlands Meteorological Institute, Instituto de Ciencias Humanas, Sociales y Ambientales and the UK National Maritime Museum. The principal objective of the CLIWOC project was to realise the scientific potential of naval logbook climatic data and to produce a database of daily weather observations for the world’s oceans between 1750 and 1850.

## Rationale (excerpt from CLIWOC documents)
From the earliest days of ocean sailing, mariners have kept accounts of their voyages. Christopher Columbus and the great Portuguese navigators began this tradition that persists to the present day. One of the principal functions of these logbooks was to assist in the navigation of the vessel. This was especially important when ships were out of sight of land and had no points of reference with which to determine their positions. By 1750 the keeping of logbooks was universal amongst the officers of European ships.

One of the factors that a ship’s officer needed to take into account for reliable navigation was the weather. Navigation became a precise science only in the nineteenth century. Before that time more approximate methods were used to determine the true direction of the vessel’s course and the distance covered each day These all required that wind force and wind direction be carefully recorded, the information being then used to determine the ‘leeway’, made by the ship. Mariners also kept a careful note of other weather phenomena such as rain, thunder, fog and snow. Because observations were made several times each day during the voyage, logbooks contain huge amounts of such detailed information.

Many logbooks failed to survive the rigours of life at sea but several thousand have come down to the present day. Some date from as long ago as the seventeenth century. Most frequent amongst the survivors are the logbooks of vessels in
state service. Many thousands have been gathered together in a number of important archives. The United Kingdom, France, Spain and the Netherlands all possess notable collections. The CLIWOC project is the first attempt at a comprehensive study of this rich source of climatic data. It is curiously ironic that this legacy of the many past wars and conflicts between these nations should offer such an opportunity for co-operative scientific endeavour in this later age.

## Understanding this information
Logbooks were written by seasoned mariners in the vocabulary unique to their profession and their times. Instruments were only rarely used and interest in the weather was limited to those aspects that influenced the navigation and progress of their ships. Seen through the eyes of the modern-day reader the descriptions of the weather are a mixture of the familiar and curious. Because the records were made to serve the needs of the day, and not those of the twenty-first century scientific enquirer, one of the principal challenges to the CLIWOC team is to interpret the weather vocabulary of former times, and thereby determine the true nature of the weather so assiduously recorded in often difficult circumstances.

There is a [dictionary](https://web.archive.org/web/20180107201509/http://webs.ucm.es/info/cliwoc/documentation/Dictionary_text.pdf) to better understand some of the records of the database and how some data was standardised between the different countries, periods, etc.

## Other similar databases
The CLIWOC database cannot claim to be the first attempt to provide a summary of marine-based climatic data. The COADS database (developed in the United States) covers the mid-nineteenth century to the present day and has an international reputation, as do the Japanese Kobe collection and the data assembled at the UK’s Hadley Centre. These databases are concerned with instrumental information only. CLIWOC’s contribution will be to extend the record of oceanic climate back by a century into the period before instruments were widely used.

## This visualization project
Even today, after some decades, I think this project was/is an amazing way to better understand where we live. It involved librarians, physicists, historians,..., to create scientific information from historical sources that is valuable to better understand the past, the present and the future.

Some technical comments: the site is done using [MapLibre](https://maplibre.org/) and a big geojson (23.8 MiB) with a lot of weather (as well as other interesting) information. The geojson file was obtained using the code in the scripts folder. The data used was downloaded from https://stvno.github.io/page/cliwoc/ (geopackage format). This dataset is a derivation of the CLIWOC v2.1 database with small changes. The script tries to reduce as much as possible the information stored in the final geojson file focusing mainly in the meteorological information thought some other interesting information has also been included to provide more context to the data. Also, the library [`antimeridian`](https://github.com/gadomski/antimeridian) is used to deal with data crossing the antimeridian and to help to have a prettier visialization of the data.

To better understand the different fields shown in the visualization and to go deeper in history, life in a ship several centuries ago and how valuable could be this information have a look to:
* Table with the different fields included in the database: https://stvno.github.io/page/cliwoc/
* dictionary: https://web.archive.org/web/20180107201509/http://webs.ucm.es/info/cliwoc/documentation/Dictionary_text.pdf
* Final report: https://web.archive.org/web/20171209023706/http://webs.ucm.es/info/cliwoc/documentation/Cliwoc_final_report.pdf
* Other references: see links section below.

P.D.: I worked in some way and veeeeeery tangentially at the later stage of this project: helping with some documents, adding some stuff to the web, visiting some of the archives.

## Links

Official project web page: https://web.archive.org/web/20220820064149/http://webs.ucm.es/info/cliwoc/
KNMI CLIWOC web page: https://web.archive.org/web/20171219105541/http://projects.knmi.nl/cliwoc/
Data used for this visualization project: https://stvno.github.io/page/cliwoc/ (gpkg file)
Database release v1.5: https://web.archive.org/web/20171029092037/http://webs.ucm.es/info/cliwoc/cliwoc15.htm
Database release v2.1: https://web.archive.org/web/20171219105603/http://projects.knmi.nl/cliwoc/download/cliwoc21.htm
CLIWOC final report: https://web.archive.org/web/20171209023706/http://webs.ucm.es/info/cliwoc/documentation/Cliwoc_final_report.pdf
Some scientific results: https://web.archive.org/web/20160515133311/http://projects.knmi.nl/cliwoc/cliwocdata.htm
Other scientific references: https://web.archive.org/web/20160515134559/http://projects.knmi.nl/cliwoc/cliwocpub.htm
Interesting site about historical climatology: https://www.historicalclimatology.com/cliwoc.html
