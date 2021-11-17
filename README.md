# Tapahtumasovellus

Projekti on luotu Helsingin Yliopiston Tietokantasovellus-kurssia varten.

Sovelluksen avulla voi luoda tapahtumia, joihin voi kutsua muita käyttäjiä. Käyttäjä voi myös etsiä julkisia tapahtumia. Käyttäjä voi ilmoittautua osallistuvansa tapahtumaan tai perua osallistumisen. Käyttäjä voi olla joko peruskäyttäjä tai ylläpitäjä.

### Sovelluksen ominaisuuksia ovat:

- Käyttäjä voi luoda uuden tunnuksen
- Käyttäjä voi kirjautua sisään ja ulos
- Käyttäjä näkee etusivulla omat tapahtumat (luodut tapahtumat sekä tapahtumat joihin on kutsuttuna)
- Käyttäjä voi luoda uuden tapahtuman, jolla on kuvaus, paikka ja aika
- Luodun tapahtuman voi rajata julkiseksi/yksityiseksi
- Käyttäjä voi muokata omaa tapahtumaansa tai poistaa oman tapahtumansa
- Käyttäjä voi etsiä muita käyttäjiä (käyttäjätunnuksia)
- Käyttäjä voi luoda käyttäjäryhmiä, joihin kuuluu muita käyttäjiä
- Käyttäjä voi kutsua muita käyttäjiä tai käyttäjäryhmiä tapahtumaansa
- Käyttäjä voi ilmoittaa osallistuvansa tai olevansa osallistumatta tapahtumaan, valintoja voi myös muuttaa
- Käyttäjä voi lähettää kommentin tapahtumasivulle
- Käyttäjä voi poistaa kommentteja omasta tapahtumastaan
- Käyttäjä voi poistaa oman kommenttinsa tai muokata sitä
- Käyttäjä voi etsiä julkisia tapahtumia nimen/luokan/paikan perusteella
- Ylläpitäjä voi luoda ja muokata luokkia, joihin julkisia tapahtumia voi luokitella
- Ylläpitäjä voi poistaa tapahtumia ja kommentteja sekä muokata niiden tietoja

### Tietokannan määrittely

Käyttäjien tiedot tallennetaan *Users*-tauluun. Käyttäjällä on käyttäjän yksilöivä id sekä käyttäjän itsensä luoma uniikki käyttäjätunnus. Taulussa on käyttäjän salasana sekä tieto siitä, onko käyttäjä ylläpitäjä vai tavallinen käyttäjä. 

Tapahtumat tallennetaan *Events*-tauluun. Tapahtumalla on tapahtuman yksilöivä id sekä järjestäjä. Tapahtuma voi olla joko julkinen tai yksityinen, jolloin se on näkyvillä ainoastaan tapahtumaan kutsutuille. Ainoastaan tapahtuman järjestäjä voi kutsua muita käyttäjiä yksityiseen tapahtumaan. Kaikki voivat kutsua muita käyttäjiä julkiseen tapahtumaan. Tapahtumalla on myös kuvaus, paikka, päivämäärä, alkamisaika ja päättymisaika. Lisäksi tapahtumalle voi määritellä kaupungin ja luokan, joilla käyttäjät voivat etsiä julkisia tapahtumia.

Luokat tallennetaan *Categories*-tauluun. Luokalla on luokan yksilöivä id, nimi ja kuvaus. Tapahtuma voi kuulua ainoastaan yhteen luokkaan mutta yhteen luokkaan voi kuulua useita tapahtumia (1-n).

Käyttäjällä voi olla useita omia tapahtumia, mutta yhdellä tapahtumalla on vain yksi järjestäjä (1-n). 

Käyttäjä voi olla kutsuttuna useampaan tapahtumaan ja tapahtumaan voi kutsua useita käyttäjiä (n-n). Tieto kutsutusta käyttäjistä tallennetaan *Invitees*-tauluun. Tauluun tallennetaan tapahtuman tunnus ja käyttäjän tunnus.

Käyttäjä voi osallistua useampaan tapahtumaan ja tapahtumaan voi osallistua useita käyttäjiä (n-n). Tieto osallistuvista käyttäjistä tallennetaan *Attendance*-tauluun. Tauluun tallennetaan tapahtuman tunnus ja käyttäjän tunnus sekä lisäksi käyttäjän vastaus, joka voi olla joko osallistuu tai ei osallistu.

Käyttäjät voivat kuulua myös ryhmiin, jotka ovat yksityisiä. Ryhmät tallennetaan *Groups*-tauluun. Ryhmällä on ryhmän yksilöivä id, nimi ja kuvaus. Lisäksi ryhmällä on perustaja, joka on ryhmän ylläpitäjä ja voi poistaa/lisätä käyttäjiä.

Käyttäjä voi kuulua useampaan ryhmään ja ryhmään voi kuulua useita käyttäjiä (n-n). Tieto ryhmään kuulumisesta tallennetaan *Members*-tauluun. Tauluun tallennetaan ryhmän tunnus sekä käyttäjän tunnus.

Tapahtumasivulle lähetettävät kommentit tallennetaan *Comments*-tauluun. Kommenteilla on kommentin yksilöivä tunnus sekä kommentin sisältö tekstinä. Jokainen tapahtuma kuuluu yhteen tapahtumaan ja sillä on yksi kirjoittaja, siis tauluun tallennetaan tapahtuman tunnus sekä lähettävän käyttäjän tunnus.

Sovelluksen tietokantakaavio löytyy schema.sql-tiedostosta.

