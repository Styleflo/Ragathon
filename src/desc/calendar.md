# calendar.txt

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


Identifiant de service calendrier associé au trajet.