## Table of contents
* [Opis](#opis)
* [Technologie](#technologie)
* [instalacja](#instalacja)

## Opis
This project is simple Lorem ipsum dolor generator.
	
## Technologie
Project is created with:
* Lorem version: 12.3
* Ipsum version: 2.33
* Ament library version: 999
	
## instalacja


```
1. Stwórz wirtualne środowisko i doinstaluj zależności z pliku requirements.txt
2. Aktywuj wirtualne środowisko
3. Przejdź do katalogu HomeworkCentre i wykonaj następujące polecenia:
	3.1: python manage.py makemigrations
	3.2: python manage.py migrate
	3.3: python manage.py create_groups
4. Stwórz administratora systemu poleceniem python manage.py createsuperuser. Postępuj zgodnie z wyświetlaną instrukcją

------------------------------------------------------------------------------------------------------------------------
							OPCJONALNE
5. Domyślnie powiadomienia email zostały wyłączone. Aby je włączyć należy:
	5.1: Ustawić  i odkomentować ustawienia konfiguracyjne w pliku HomeworkCentre/HomeworkCentre/settings.py, znajdujące się na końcu pliku (ustawienia z przedrostkiem EMAIL)
	5.2 Odkomentować zawartość plików HomeworkCentre/User/signals.py oraz HomeworkCentre/Homework/signals.py
--------------------------------------------------------------------------------------------------------------------------

6. Uruchom serwer poleceniem python manage.py runserver z katalogu HomeworkCentre

UWAGA! Kroki 1-5 należy wykonać tylko raz, podczas pierwszego uruchomienia aplikacji.
```



