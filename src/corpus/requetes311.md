# requetes311.csv

## ID_UNIQUE
### Alphanumeric / Identifier
#### N/A
Identifiant unique de la demande. Note : Cette donnée n'est pas disponible pour les demandes d'informations générales (NATURE = "Information").

## NATURE
### Enumeration
#### Information, Commentaire, Requête, Plainte
Type de la demande:
* Information (Générale – prestation) : Toute demande d’un citoyen pour obtenir une information ou un document (dépliant, brochure, formulaire, etc.), étant satisfaite immédiatement et par conséquent ne nécessitant aucun suivi. Cette catégorie englobe aussi les prestations ne requérant aucun suivi particulier (vente d’un produit, encaissement d’un compte de taxes ou d’un constat d’infraction, etc.). De plus, cette catégorie englobe toute demande visant à obtenir une information de la part d’un spécialiste d’un arrondissement ou d’un service corporatif.
* Commentaire (Commentaire – suggestion) : Tout commentaire, suggestion ou proposition exprimant l’opinion d’un citoyen sur une question de compétence municipale. L’administration en tient compte sans pour autant poser une action immédiate.
* Requête : Toute demande d’un citoyen visant à obtenir une autorisation (permis, etc.), un soutien (subvention, etc.), un service (inspection, réparation, etc.) ou un autre type d’intervention de la Ville. Cette catégorie inclut les réclamations des citoyens.
* Plainte : Toutes doléances d’un citoyen à l’égard des services municipaux, du comportement des gestionnaires ou employés municipaux pour une prestation de service inadéquate, d'une absence de prestation de service, d'un acte inacceptable, d'une infraction, d'un abus de pouvoir ou d'une discrimination, etc.

## ACTI_NOM
### Text
#### N/A
Catégorie de la demande ou nom de l'activité associée.

## TYPE_LIEU_INTERV
### Text
#### N/A
Indication sur l'association géographique initiale de la demande.

## ARRONDISSEMENT
### Text
#### N/A
Arrondissement officiellement attitré pour prendre en charge et régler la requête.

## ARRONDISSEMENT_GEO
### Text
#### N/A
Arrondissement (géographiquement parlant) dans lequel l'intervention doit avoir lieu.

## UNITE_RESP_PARENT
### Text
#### N/A
Unité responsable parente chargée du dossier.

## DDS_DATE_CREATION
### Date and Time
#### N/A
Date et heure de création de l'événement dans le système.

## PROVENANCE_ORIGINALE
### Text
#### N/A
Canal de provenance de la communication initiale.

## PROVENANCE_TELEPHONE
### Integer
#### N/A
Nombre de requérants différents ayant utilisé le téléphone (311).

## PROVENANCE_COURRIEL
### Integer
#### N/A
Nombre de requérants différents ayant communiqué via courriel.

## PROVENANCE_PERSONNE
### Integer
#### N/A
Nombre de requérants différents s'étant présentés en personne au bureau Accès Montréal.

## PROVENANCE_COURRIER
### Integer
#### N/A
Nombre de requérants différents ayant communiqué via courrier postal.

## PROVENANCE_TELECOPIEUR
### Integer
#### N/A
Nombre de requérants différents ayant communiqué via télécopieur.

## PROVENANCE_INSTANCE
### Integer
#### N/A
Nombre de requérants différents provenant d'une instance officielle.

## PROVENANCE_MOBILE
### Integer
#### N/A
Nombre de requérants différents ayant utilisé l'application mobile.

## PROVENANCE_MEDIASOCIAUX
### Integer
#### N/A
Nombre de requérants différents ayant communiqué via les médias sociaux.

## PROVENANCE_SITEINTERNET
### Integer
#### N/A
Nombre de requérants différents ayant utilisé le portail web (site internet).

## RUE
### Text
#### N/A
Rue concernée par la demande de service.

## RUE_INTERSECTION1
### Text
#### N/A
Nom de la première rue formant l'intersection adjacente au lieu d'intervention.

## RUE_INTERSECTION2
### Text
#### N/A
Nom de la seconde rue formant l'intersection adjacente au lieu d'intervention.

## LIN_CODE_POSTAL
### Alphanumeric
#### N/A
Code postal concerné par la demande.

## LOC_X
### Numeric
#### N/A
Coordonnée X (système NAD83 MTM Zone 8). Note : La position est volontairement obfusquée.

## LOC_Y
### Numeric
#### N/A
Coordonnée Y (système NAD83 MTM Zone 8). Note : La position est volontairement obfusquée.

## LOC_LAT
### Numeric
#### N/A
Latitude géographique. Note : La position est volontairement obfusquée.

## LOC_LONG
### Numeric
#### N/A
Longitude géographique. Note : La position est volontairement obfusquée.

## LOC_ERREUR_GDT
### Numeric Code
#### 0, 1
Information sur la précision du positionnement de la requête avant l'obfuscation : 0 = localisation au lieu exact de la requête, 1 = localisation par défaut au BAM de l'arrondissement.

## DERNIER_STATUT
### Enumeration
#### Acceptée, Annulée, Prise en charge, Réactivée, Refusée, Supprimée, Terminée, Transmise pour traitement, Urgente
Dernier état associé à une demande

## DATE_DERNIER_STATUT
### Date and Time
#### N/A
Date associée au moment où le dernier état (DERNIER_STATUT) a été appliqué à la demande.