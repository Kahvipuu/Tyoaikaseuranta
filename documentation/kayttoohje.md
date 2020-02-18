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

## Puuttuvat ominaisuudet
Toistaiseksi eri käyttäjäluokat ainakin puuttuvat, sekä tietenkin niihin liittyvät toiminnallisuudet.

## Käyttötapaukset / user storyt ja niihin liittyvät SQL-kyselyt
Käyttötapaukset ja User storyt ovat omassa dokumentissaan. 

Toistaiseksi monimitkaisin sql-kysely on projektien tuntikirjausten projektikohtainen tuntimäärä:
"SELECT project.name, SUM(worktimerecord.hours) FROM Account"
" LEFT JOIN worktimerecord ON worktimerecord.account_id = Account.id"
" LEFT JOIN project ON project.id = worktimerecord.project_id"
" GROUP BY project.id"

## Tietokantarakenteen kuvaus
Kuvat tietokantarakenteen kehityksestä löytyvät omasta dokumentistaan.
Tämän hetken tilanne rakenteessa on seuraava:

CREATE TABLE account (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        username VARCHAR(144) NOT NULL,
        password VARCHAR(144) NOT NULL,
        PRIMARY KEY (id)
);
CREATE TABLE project (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        active BOOLEAN NOT NULL,
        leader VARCHAR(144) NOT NULL,
        projectlead_account_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        CHECK (active IN (0, 1)),
        FOREIGN KEY(projectlead_account_id) REFERENCES account (id)
);
CREATE TABLE worktimerecord (
        id INTEGER NOT NULL,
        date_created DATETIME,
        date_modified DATETIME,
        name VARCHAR(144) NOT NULL,
        done BOOLEAN NOT NULL,
        hours INTEGER,
        dateofwork DATE,
        account_id INTEGER NOT NULL,
        project_name VARCHAR(144),
        project_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        CHECK (done IN (0, 1)),
        FOREIGN KEY(account_id) REFERENCES account (id),
        FOREIGN KEY(project_id) REFERENCES project (id)
);