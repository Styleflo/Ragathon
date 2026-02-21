# gtfs_stm.csv

## agency_id

### string(id)

#### STM

Identifiant unique de l’agence (ex.: STM).

## agency_name

### string

#### Société de transport de Montréal

Nom de l’agence de transport.

## agency_url

### string

#### https://www.stm.info

Site web de l’agence.

## agency_timezone

### time(HH:MM:SS)

#### America/Montreal

Fuseau horaire de l’agence (IANA).

## agency_lang

### string

#### fr

Langue principale de l’agence (code ISO).

## agency_phone

### string

#### 

Téléphone de contact de l’agence.

## agency_fare_url

### string

#### https://www.stm.info/fr/tarifs

Page web décrivant les tarifs de l’agence.

## service_id

### string(id)

#### 

Identifiant du service (référence utilisée par trips).

## monday

### int(enum/flag)

#### 1, 0

Indique si le service est actif le lundi (0/1).

## tuesday

### int(enum/flag)

#### 1, 0

Indique si le service est actif le mardi (0/1).

## wednesday

### int(enum/flag)

#### 1, 0

Indique si le service est actif le mercredi (0/1).

## thursday

### int(enum/flag)

#### 1, 0

Indique si le service est actif le jeudi (0/1).

## friday

### int(enum/flag)

#### 1, 0

Indique si le service est actif le vendredi (0/1).

## saturday

### int(enum/flag)

#### 0, 1

Indique si le service est actif le samedi (0/1).

## sunday

### int(enum/flag)

#### 0, 1

Indique si le service est actif le dimanche (0/1).

## start_date

### date(YYYYMMDD)

#### 

Date de début de validité du service (YYYYMMDD).

## end_date

### date(YYYYMMDD)

#### 

Date de fin de validité du service (YYYYMMDD).

## service_id

### string(id)

#### 

Identifiant du service concerné.

## date

### date(YYYYMMDD)

#### 20260307, 20260308, 20260302, 20260303, 20260304, 20260305, 20260306, 20251225

Date d’exception (YYYYMMDD).

## exception_type

### int(enum/flag)

#### 2

Type d’exception (ex.: ajout ou suppression du service).

## feed_publisher_name

### string

#### Société de transport de Montréal

Nom de l’éditeur du flux (publisher).

## feed_publisher_url

### string

#### https://www.stm.info

URL de l’éditeur du flux.

## feed_lang

### string

#### fr

Langue principale du flux (code ISO).

## feed_start_date

### date(YYYYMMDD)

#### 20251027

Date de début de couverture du flux (YYYYMMDD).

## feed_end_date

### date(YYYYMMDD)

#### 20260322

Date de fin de couverture du flux (YYYYMMDD).

## feed_version

### string

#### 20260211151500_26J

Version du flux (identifiant de build).

## route_id

### string(id)

#### 

Identifiant unique de la ligne (route).

## agency_id

### string(id)

#### STM

Identifiant de l’agence opérant la ligne.

## route_short_name

### int

#### 

Nom court / numéro de ligne.

## route_long_name

### string

#### 

Nom long de la ligne.

## route_type

### int(enum/flag)

#### 1, 3

Type de transport (ex.: métro, bus).

## route_url

### string

#### https://www.stm.info/fr/infos/reseaux/metro/ligne-1---verte, https://www.stm.info/fr/infos/reseaux/metro/ligne-2---orange, https://www.stm.info/fr/infos/reseaux/metro/ligne-4---jaune, https://www.stm.info/fr/infos/reseaux/metro/ligne-5---bleue, https://www.stm.info/fr/infos/reseaux/bus, http://www.stm.info/fr/infos/reseaux/bus

Liste des lignes des autobus Champ `route_url`.

## route_color

### string(hex RGB)

#### 00B300, D95700, FFD900, 0095E6, 009EE0, 781B7D, 034638

Couleur de la ligne (hex RGB sans #).

## route_text_color

### string(hex RGB)

#### FFFFFF, 000000

Couleur du texte (hex RGB sans #).

## shape_id

### string(id)

#### 

Identifiant unique de la forme (géométrie du parcours).

## shape_pt_lat

### float

#### 

Latitude d’un point du tracé (WGS84).

## shape_pt_lon

### float

#### 

Longitude d’un point du tracé (WGS84).

## shape_pt_sequence

### int

#### 

Ordre (séquence) du point dans le tracé.

## trip_id

### string(id)

#### 

Identifiant du trajet (trip) auquel l’arrêt-temps appartient.

## arrival_time

### time(HH:MM:SS)

#### 

Heure d’arrivée à l’arrêt (HH:MM:SS).

## departure_time

### time(HH:MM:SS)

#### 

Heure de départ de l’arrêt (HH:MM:SS).

## stop_id

### string(id)

#### 

Identifiant de l’arrêt.

## stop_sequence

### int

#### 

Ordre de passage des arrêts dans le trajet (1..n).

## pickup_type

### int(enum/flag)

#### 0, 1

Règle de prise en charge (pickup) à l’arrêt.

## stop_id

### string(id)

#### 

Identifiant unique de l’arrêt.

## stop_code

### int

#### 

Code public de l’arrêt (si applicable).

## stop_name

### string

#### 

Nom de l’arrêt.

## stop_lat

### float

#### 

Latitude de l’arrêt (WGS84).

## stop_lon

### float

#### 

Longitude de l’arrêt (WGS84).

## stop_url

### string

#### 

Liste des arrêts d’autobus Champ `stop_url`.

## location_type

### int(enum/flag)

#### 1, 0, 2

Type d’emplacement (ex.: stop, station).

## parent_station

### string

#### 

Identifiant de la station parent (si applicable).

## wheelchair_boarding

### int(enum/flag)

#### 1, 2

Accessibilité PMR (embarquement fauteuil roulant).

## route_id

### string(id)

#### 

Identifiant de la ligne associée au trajet (route).

## service_id

### string(id)

#### 

Identifiant de service calendrier associé au trajet.

## trip_id

### string(id)

#### 

Identifiant unique du trajet (trip).

## trip_headsign

### string

#### 

Destination / headsign affiché pour le trajet.

## direction_id

### string(id)

#### 0, 1

Direction du trajet (souvent 0/1).

## shape_id

### string(id)

#### 

Identifiant de la géométrie (shape) associée au trajet.

## wheelchair_accessible

### int(enum/flag)

#### 1, 2

Indique l’accessibilité fauteuil roulant du trajet.

## note_fr

### string

#### 

Information concernant l’horaire de voyages Champ `note_fr`.

## note_en

### string

#### 

Information concernant l’horaire de voyages Champ `note_en`.

## table_name

### string

#### agency, routes, stops, trips

Nom de la table GTFS concernée par la traduction.

## field_name

### string

#### agency_fare_url, route_url, route_long_name, stop_url, stop_name, trip_headsign

Nom du champ concerné par la traduction.

## language

### string

#### en

Langue de la traduction (code ISO).

## record_id

### string(id)

#### 

Identifiant de l’enregistrement (ex.: route_id, agency_id).

## translation

### string

#### 

Valeur traduite.
