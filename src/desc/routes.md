# routes.txt

## route_id

### string(id)

#### 


Identifiant unique de la ligne (route).

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

## route_id

### string(id)

#### 


Identifiant de la ligne associée au trajet (route).