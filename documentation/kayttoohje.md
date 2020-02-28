# Työaikaseuranta, käyttöohje

Sovellukseen voi kirjautua oikeasta yläkulmasta.
Kirjautumisen vieressä on myös uusille käyttäjille rekisteröitymismahdollisuus.
Yläreunasta löytyy muutenkin kaikkien käyttötapauksien linkit

Ohjelmaan on luotava projekti ennenkuin sille voi lisätä tuntikirjauksia. Projektin luojasta tulee samalla automaattisesti sen projektipäällikkö.

## Asennusohje

### Omalla koneella käyttäminen
Pythonin virtuaaliympäristö tarvitaan toistaiseksi ohjelman paikalliseen käyttöön. Requirements.txt sisältää ohjelman tämänhetkisest riipuvuudet, jotka tulee asentaa (sekä lisäksi pkg-resources==0.0.0, joka on poistettu Herokun takia).

### Herokussa käyttäminen
Herokussa ohjelman saa toimimaan kloonaamalla sen omalle koneelleen, tekemällä Heroku tunnukset ja vaikka tekemällä ohjelmasta itselleen uuden repositorion. Heroku tarvitsee myös tietokannan, jonka saa esim. komennolla "heroku addons:add heroku-postgresql:hobby-dev".
