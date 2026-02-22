# collisions_routieres.csv

## AN
### Num
#### AAAA
Année de l'accident au format AAAA.

## NO_SEQ_COLL
### Alph
#### AAAA _ 999
Numéro séquentiel identifiant l'accident, composé de l'année et d'un numéro séquentiel séparés par un espace et une barre de soulignement.

## DT_ACCDN
### Alph
#### AAAA-MM-JJ
Date précise de l'accident au format année-mois-jour.

## HR_ACCDN
### Alph
#### 20:00:00-20:59:59
Heure de l'accident présentée par intervalle de 60 minutes.

## JR_SEMN_ACCDN
### Alph
#### DI (Dimanche), TU (Lundi), MA (Mardi), ME (Mercredi), JE (Jeudi), VE (Vendredi), SA (Samedi)
Jour de la semaine : Dimanche, Lundi, Mardi, Mercredi, Jeudi, Vendredi, Samedi.

## GRAVITÉ
### Alph
#### Mortel, Grave, Léger, Dommages matériels seulement
Indique la gravité de l'accident selon l'état des victimes ou l'importance des dommages matériels.

## NB_MORTS
### Num
#### N/A
Nombre de victimes décédées dans les 30 jours suivant l'accident.

## NB_BLESSES_GRAVES
### Num
#### N/A
Nombre de victimes blessées gravement nécessitant une hospitalisation.

## NB_BLESSES_LEGERS
### Num
#### N/A
Nombre de victimes blessées légèrement ne nécessitant pas d'hospitalisation.

## NB_VICTIMES_TOTAL
### Num
#### N/A
Somme totale des décès, blessés graves et blessés légers.

## NB_VEH_IMPLIQUES_ACCDN
### Num
#### N/A
Nombre total de véhicules impliqués dans l'accident.

## NB_DECES_PIETON
### Num
#### N/A
Nombre de piétons décédés suite à l'accident.

## NB_BLESSES_PIETON
### Num
#### N/A
Nombre de piétons blessés (graves ou légers) dans l'accident.

## NB_VICTIMES_PIETON
### Num
#### N/A
Nombre total de victimes parmi les piétons dand l'accident.

## NB_DECES_MOTO
### Num
#### N/A
Nombre de motocyclistes décédés dans l'accident.

## NB_BLESSES_MOTO
### Num
#### N/A
Nombre de motocyclistes blessés dans l'accident.

## NB_VICTIMES_MOTO
### Num
#### N/A
Nombre total de victimes parmi les motocyclistes.

## NB_DECES_VELO
### Num
#### N/A
Nombre de cyclistes décédés.

## NB_BLESSES_VELO
### Num
#### N/A
Nombre de cyclistes blessés.

## NB_VICTIMES_VELO
### Num
#### N/A
Nombre total de victimes parmi les cyclistes.

## CD_MUNCP
### Alph
#### N/A
Code géographique de la municipalité où l'accident a eu lieu.

## MRC
### Alph
#### N/A
Nom de la municipalité régionale de comté (MRC).

## NO_CIVIQ_ACCDN
### Alph
#### N/A
Numéro civique de l'immeuble le plus proche du lieu de l'impact.

## SFX_NO_CIVIQ_ACCDN
### Alph
#### N/A
Suffixe du numéro civique de l'immeuble (ex: A, B).

## RUE_ACCDN
### Alph
#### N/A
Nom de la rue, du rang ou du chemin du lieu de l'accident.

## REG_ADM
### Alph
#### 01 (Bas-Saint-Laurent), 02 (Saguenay―Lac-Saint-Jean), 03 (Capitale-Nationale), 04 (Mauricie), 05 (Estrie), 06 (Montréal), 07 (Outaouais), 08 (Abitibi-Témiscamingue), 09 (Côte-Nord), 10 (Nord-du-Québec), 11 (Gaspésie―Îles-de-la-Madeleine), 12 (Chaudière-Appalaches), 13 (Laval), 14 (Lanaudière), 15 (Laurentides), 16 (Montérégie), 17 (Centre-du-Québec)
Région administrative du Québec (ex: Montréal, Estrie, Laurentides).

## ACCDN_PRES_DE
### Alph
#### N/A
Nom de la rue transversale pour une intersection ou nom d'un repère (école, commerce).

## NO_ROUTE
### Alph
#### N/A
Numéro de la route numérotée où l'accident est survenu.

## BORNE_KM_ACCDN
### Num
#### N/A
Numéro de la borne kilométrique la plus proche de l'accident.

## NB_METRE_DIST_ACCD
### Num
#### N/A
Distance en mètres entre le lieu de l'accident et le repère ou numéro civique indiqué.

## VITESSE_AUTOR
### Num
#### N/A
Vitesse maximale permise en km/h sur la route concernée.

## TP_REPRR_ACCDN
### Alph
#### 1 (Intersection), 2 (Autre repère), 0 (Non précisé)
Code du type de repère : Intersection, Autre repère, Non précisé.

## CD_PNT_CDRNL_REPRR
### Alph
#### N, S, E, O
Point cardinal situant l'accident par rapport au repère.

## CD_PNT_CDRNL_ROUTE
### Alph
#### N, S, E, O
Direction attachée au numéro de la route pour les voies séparées.

## CD_GENRE_ACCDN
### Alph
#### 31 (Collision avec véhicule), 32 (piéton), 40-54 (objet fixe), 71 (capotage)
Nature de l'impact (ex: Collision avec véhicule, piéton, objet fixe, capotage).

## CD_SIT_PRTCE_ACCDN
### Alph
#### 1 (Déversement), 2 (Perte de chargement), 3 (Déneigement)
Situations spéciales : Déversement, Perte de chargement, Déneigement.

## CD_ETAT_SURFC
### Alph
#### 11 (Sèche), 12 (Mouillée), 16 (Enneigée), 18 (Glacée), 19 (Boueuse)
Condition de la surface (ex: Sèche, Mouillée, Enneigée, Glacée, Boueuse).

## CD_ECLRM
### Alph
#### 1 (Jour), 2 (Demi-obscurité), 3 (Nuit éclairée), 4 (Nuit non éclairée)
Niveau de luminosité : Jour, Demi-obscurité, Nuit éclairée, Nuit non éclairée.

## CD_ENVRN_ACCDN
### Alph
#### 1 (Scolaire), 2 (Résidentiel), 3 (Commercial), 5 (Rural)
Activité dominante du secteur (ex: Scolaire, Résidentiel, Commercial, Rural).

## CD_CATEG_ROUTE
### Alph
#### 11 (Autoroute), 12 (Route numérotée), 14 (Rue résidentielle), 21 (Stationnement)
Type de route (ex: Autoroute, Route numérotée, Rue résidentielle, Stationnement).

## CD_ETAT_CHASS
### Alph
#### 1 (Bon état), 2 (En construction), 5 (Trous/nids-de-poule)
État physique de la route : Bon état, En construction, Trous/nids-de-poule.

## CD_ASPCT_ROUTE
### Alph
#### 11 (Droit et plat), 13 (Droit en pente), 21 (Courbe et plat)
Géométrie de la route (ex: Droit et plat, Droit en pente, Courbe et plat).

## CD_LOCLN_ACCDN
### Alph
#### 32 (Intersection), 35 (Passage à niveau), 36 (Pont), 38 (Tunnel)
Emplacement longitudinal (ex: Intersection, Passage à niveau, Pont, Tunnel).

## CD_POSI_ACCDN
### Alph
#### 1 (Voie réservée), 6 (Voie de circulation), 7 (Accotement), 9 (Trottoir)
Localisation transversale (ex: Voie réservée, Voie de circulation, Accotement, Trottoir).

## CD_CONFG_ROUTE
### Alph
#### 1 (Sens unique), 2-3 (Deux sens), 4-5 (Séparée)
Aménagement des voies : Sens unique, Deux sens, Séparée.

## CD_ZON_TRAVX_ROUTR
### Alph
#### 1 (Aux approches de la zone), 2 (Dans la zone)
Indique si l'accident a eu lieu aux approches ou dans une zone de travaux.

## CD_COND_METEO
### Alph
#### 11 (Clair), 12 (Nuageux), 14 (Pluie), 17 (Neige), 19 (Verglas)
Conditions Météorologiques. Conditions atmosphériques présentes lors de l’accident. (ex: Clair, Nuageux, Pluie, Neige, Verglas).

## nb_automobile_camion_leger
### Num
#### N/A
Nombre d'autos ou camions légers impliqués dans l'accident.

## nb_camionLourd_tractRoutier
### Num
#### N/A
Nombre de véhicules lourds impliqués dans l'accident.

## nb_outil_equipement
### Num
#### N/A
Nombre de véhicules-outils ou équipements impliqués dans l'accident.

## nb_tous_autobus_minibus
### Num
#### N/A
Nombre d'autobus ou minibus (incluant scolaires) impliqués dans l'accident.

## nb_bicyclette
### Num
#### N/A
Nombre de vélos impliqués dans l'accident.

## nb_cyclomoteur
### Num
#### N/A
Nombre de cyclomoteurs impliqués dans l'accident.

## nb_motocyclette
### Num
#### N/A
Nombre de motos impliquées dans l'accident.

## nb_taxi
### Num
#### N/A
Nombre de taxis impliqués dans l'accident.

## nb_urgence
### Num
#### N/A
Nombre de véhicules d'urgence impliqués dans l'accident.

## nb_motoneige
### Num
#### N/A
Nombre de motoneiges impliquées dans l'accident.

## nb_VHR
### Num
#### N/A
Nombre de VHR ou motocyclettes hors route impliqués dans l'accident

## nb_autres_types
### Num
#### N/A
Nombre de véhicules d’un autre type impliqués dans l'accident
## nb_veh_non_precise
### Num
#### N/A
Nombre de véhicules de type non précisé impliqués dans l'accident