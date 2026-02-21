# Dataset : requetes311.csv

## Nom de la colonne : ID_UNIQUE
### Type de valeur : Alphanumérique / Identifiant
#### Énumération : N/A
Identifiant unique de la demande. Note : Cette donnée n'est pas disponible pour les demandes d'informations générales (NATURE = "Information").


## Nom de la colonne : NATURE
### Type de valeur : Énumération
#### Énumération : Information, Commentaire, Requête, Plainte
##### Type de la demande. 
* Information (Générale – prestation) : Toute demande d’un citoyen pour obtenir une information ou un document (dépliant, brochure, formulaire, etc.), étant satisfaite immédiatement et par conséquent ne nécessitant aucun suivi. Cette catégorie englobe aussi les prestations ne requérant aucun suivi particulier (vente d’un produit, encaissement d’un compte de taxes ou d’un constat d’infraction, etc.). De plus, cette catégorie englobe toute demande visant à obtenir une information de la part d’un spécialiste d’un arrondissement ou d’un service corporatif.
* Commentaire (Commentaire – suggestion) : Tout commentaire, suggestion ou proposition exprimant l’opinion d’un citoyen sur une question de compétence municipale. L’administration en tient compte sans pour autant poser une action immédiate.
* Requête : Toute demande d’un citoyen visant à obtenir une autorisation (permis, etc.), un soutien (subvention, etc.), un service (inspection, réparation, etc.) ou un autre type d’intervention de la Ville. Cette catégorie inclut les réclamations des citoyens.
* Plainte : Toutes doléances d’un citoyen à l’égard des services municipaux, du comportement des gestionnaires ou employés municipaux pour une prestation de service inadéquate, d'une absence de prestation de service, d'un acte inacceptable, d'une infraction, d'un abus de pouvoir ou d'une discrimination, etc.

## Nom de la colonne : ACTI_NOM
### Type de valeur : Texte
#### Énumération : N/A
Catégorie de la demande ou nom de l'activité associée.

## Nom de la colonne : TYPE_LIEU_INTERV
### Type de valeur : Texte
#### Énumération : N/A
Indication sur l'association géographique initiale de la demande.

## Nom de la colonne : ARRONDISSEMENT
### Type de valeur : Texte
#### Énumération : N/A
Arrondissement officiellement attitré pour prendre en charge et régler la requête.

## Nom de la colonne : ARRONDISSEMENT_GEO
### Type de valeur : Texte
#### Énumération : N/A
Arrondissement (géographiquement parlant) dans lequel l'intervention doit avoir lieu.

## Nom de la colonne : UNITE_RESP_PARENT
### Type de valeur : Texte
#### Énumération : N/A
Unité responsable parente chargée du dossier.

## Nom de la colonne : DDS_DATE_CREATION
### Type de valeur : Date et Heure
#### Énumération : N/A
Date et heure de création de l'événement dans le système.

## Nom de la colonne : PROVENANCE_ORIGINALE
### Type de valeur : Texte
#### Énumération : N/A
Canal de provenance de la communication initiale.

## Nom de la colonne : PROVENANCE_TELEPHONE
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant utilisé le téléphone (311).

## Nom de la colonne : PROVENANCE_COURRIEL
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant communiqué via courriel.

## Nom de la colonne : PROVENANCE_PERSONNE
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents s'étant présentés en personne au bureau Accès Montréal.

## Nom de la colonne : PROVENANCE_COURRIER
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant communiqué via courrier postal.

## Nom de la colonne : PROVENANCE_TELECOPIEUR
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant communiqué via télécopieur.

## Nom de la colonne : PROVENANCE_INSTANCE
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents provenant d'une instance officielle.

## Nom de la colonne : PROVENANCE_MOBILE
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant utilisé l'application mobile.

## Nom de la colonne : PROVENANCE_MEDIASOCIAUX
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant communiqué via les médias sociaux.

## Nom de la colonne : PROVENANCE_SITEINTERNET
### Type de valeur : Entier
#### Énumération : N/A
Nombre de requérants différents ayant utilisé le portail web (site internet).

## Nom de la colonne : RUE
### Type de valeur : Texte
#### Énumération : N/A
Rue concernée par la demande de service.

## Nom de la colonne : RUE_INTERSECTION1
### Type de valeur : Texte
#### Énumération : N/A
Nom de la première rue formant l'intersection adjacente au lieu d'intervention.

## Nom de la colonne : RUE_INTERSECTION2
### Type de valeur : Texte
#### Énumération : N/A
Nom de la seconde rue formant l'intersection adjacente au lieu d'intervention.

## Nom de la colonne : LIN_CODE_POSTAL
### Type de valeur : Alphanumérique
#### Énumération : N/A
Code postal concerné par la demande.

## Nom de la colonne : LOC_X
### Type de valeur : Numérique
#### Énumération : N/A
Coordonnée X (système NAD83 MTM Zone 8). Note : La position est volontairement obfusquée.

## Nom de la colonne : LOC_Y
### Type de valeur : Numérique
#### Énumération : N/A
Coordonnée Y (système NAD83 MTM Zone 8). Note : La position est volontairement obfusquée.

## Nom de la colonne : LOC_LAT
### Type de valeur : Numérique
#### Énumération : N/A
Latitude géographique. Note : La position est volontairement obfusquée.

## Nom de la colonne : LOC_LONG
### Type de valeur : Numérique
#### Énumération : N/A
Longitude géographique. Note : La position est volontairement obfusquée.

## Nom de la colonne : LOC_ERREUR_GDT
### Type de valeur : Code numérique
#### Énumération : 0, 1
Information sur la précision du positionnement de la requête avant l'obfuscation : 0 = localisation au lieu exact de la requête, 1 = localisation par défaut au BAM de l'arrondissement.

## Nom de la colonne : DERNIER_STATUT
### Type de valeur : Énumération
#### Énumération : Acceptée, Annulée, Prise en charge, Réactivée, Refusée, Supprimée, Terminée, Transmise pour traitement, Urgente
Dernier état associé à la demande dans le cycle de vie du traitement.

## Nom de la colonne : DATE_DERNIER_STATUT
### Type de valeur : Date et Heure
#### Énumération : N/A
Date associée au moment où le dernier état (DERNIER_STATUT) a été appliqué à la demande.