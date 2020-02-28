# Ohjelman tarjoamat toiminnot

[readme](https://github.com/Kahvipuu/Tyoaikaseuranta/blob/master/README.md)

## Toiminnot:
* Kirjautuminen ohjelmaan
* Tuntikirjauksen tekeminen
* Projektin perustaminen
* Liittyminen projektiin
    - tapahtuu tekemällä projektiin tuntikirjaus
* Projektipäällikön raportit
* Projektin päättäminen
    - tätä ei toistaiseksi ole toteutettu

Käyttötapaukset:
* Käyttäjä voi luoda tunnuksen itselleen
    - SELECT account.name FROM account WHERE account.name = (name) VALUES (?);
    - riippuen ohjelmasta: setString(1, user_input_name), muissakin kyselyissä vastaava rakenne jota en jatkossa dokumentaatioon toista.
    - jos löytyy tietoannasta jo sama nimi niin käyttäjän täytyy kokeilla jotain toista.
    - INSERT INTO account (name, username, password) VALUES (form.name, form.username, form.password);

* Käyttäjä voi kirjautua ohjelmaan
    - SELECT account.id FROM account WHERE account.name = name AND account.password = password;

* Käyttäjä voi luoda uuden projektin
    - INSERT INTO project (name, boolean, leader, lead_acc_id) VALUES (form.name, 1, current.user.name, curr.user.id)
    - Halusin projektin johtajan nimen tähän käytettävyyden helpottamiseksi, käyttäjä ei voi vaihtaa nimeään joten tieto pysyy validina

* Käyttäjä voi liittyä olemassaolevaan projektiin
    - tapahtuu tekemällä tuntikirjaus

* Käyttäjä voi tehdä tuntikirjauksen itselleen
    - SELECT project.id FROM project WHERE project.id = "annettu_id"
    - INSERT INTO worktimerecord (name, hours, date, user_id, proj_name, proj_id, ) VALUES (form.name, form.hours, form.date, curr.user_id, found_project.name, form.proj_id);
    - Vaikka projektin nimeä muuttaessa joutuu käymään läpi tuntikirjaukset, niin halusin käytettävyyden takia tähän mukaan projektin nimen.

* Käyttäjä voi listata omat tuntikirjauksensa
    - SELECT * FROM worktimerecord WHERE worktimerecord.user_id = current.user.id

* Projektin omistaja/luoja voi listata kaikki projektiin kirjatut tunnit
    - haetaan projektit jossa käyttäjä johtajana.
    - SELECT * FROM project WHERE project.proj_lead_acc_id = curr.user.account_id
    - haetaan kirjaukset johdetuista projekteista.
    - SELECT * FROM worktimerecord WHERE worktimerecord.proj_id IN (projects_lead)

* Projektin omistaja voi poistaa projektin
    - Aluksi tarkistetaan onko projekti tyhjä.
    - SELECT * FROM worktimerecord WHERE wtr.project_id = given_project_id
    - Poisto jos edellinen ehto ei pysäytä metodia.
    - DELETE FROM Project WHERE Project.id = given_id
    - Olisi parempi toteuttaa tekemällä projektista passiivinen, jolloin jo tehtyjä kirjauksia ei menetetä. Nyt kirjaukset täytyy poistaa ennen kuin projektin voi poistaa.

* Työaikakirjauksen omistaja voi poistaa kirjauksen
    - DELETE FROM worktimerecord WHERE wtr.id = given_id

* Kirjauksen tai projektin tekijä voi muokata näitä
    - UPDATE taulunnimi SET sarakeX="uusiarvo", sarakeX2="uusiarvo2" WHERE taulu.id = "annettu.id";

## Puuttuvat ominaisuudet
* Toistaiseksi eri käyttäjäluokat ainakin puuttuvat, sekä tietenkin niihin liittyvät toiminnallisuudet. Kuitenkin projektin luoja on projektin johtaja oletuksena ja näkee projektista enemmän tietoa.
* Projektin päättämistä ei ole toteutettu.
* Projektiin erikseen liittyminen voisi olla suotavaa projektimäärän kasvaessa. Tähän olisi myös perusteltua toteuttaa henkilön ja projektin välinen erillinen monesta-moneen suhde. 
* Käyttäjäluokka joka näkee kaiken ohjelmaan kirjatun tiedon.

## Käyttötapaukset / user storyt ja niihin liittyvät SQL-kyselyt
Käyttötapauksiin liittyvät kyselyt on kirjattu käyttötapauksen esittelyn yhteyteen.
Monimutkaisemmat ohjelman toimintaan liittyvät kyselyt alla.

Toistaiseksi monimitkaisin sql-kysely on projektien tuntikirjausten projektikohtainen tuntimäärä:
* "SELECT project.name, SUM(worktimerecord.hours) FROM Account
* LEFT JOIN worktimerecord ON worktimerecord.account_id = Account.id
* LEFT JOIN project ON project.id = worktimerecord.project_id
* GROUP BY project.id;"

Toinen monimutkaisempi kysely on seuraava. Kyselyt täytyi toteuttaa sisäkkäin, jotta kokonaisuus toimisi oikein. Tähän en liittänyt toista taulua, vaikka alunperin oli ajatus, kun kyssely on monimutkaisempi jo sisäkkäisen rakenteen puolesta.
* "SELECT COUNT(1) FROM (SELECT account.id FROM account GROUP BY account.id);"

## Tietokantarakenteen kuvaus
Kuvat tietokantarakenteen kehityksestä löytyvät omasta dokumentistaan.
Tämän hetken tilanne rakenteessa on seuraava:

* CREATE TABLE account (
- id INTEGER NOT NULL,
- date_created DATETIME,
- date_modified DATETIME,
- name VARCHAR(144) NOT NULL,
- username VARCHAR(144) NOT NULL,
- password VARCHAR(144) NOT NULL,
- PRIMARY KEY (id));

* CREATE TABLE project (
- id INTEGER NOT NULL,
- date_created DATETIME,
- date_modified DATETIME,
- name VARCHAR(144) NOT NULL,
- active BOOLEAN NOT NULL,
- leader VARCHAR(144) NOT NULL,
- projectlead_account_id INTEGER NOT NULL,
- PRIMARY KEY (id),
- CHECK (active IN (0, 1)),
- FOREIGN KEY(projectlead_account_id) REFERENCES account (id));

* CREATE TABLE worktimerecord (
- id INTEGER NOT NULL,
- date_created DATETIME,
- date_modified DATETIME,
- name VARCHAR(144) NOT NULL,
- done BOOLEAN NOT NULL,
- hours INTEGER,
- dateofwork DATE,
- account_id INTEGER NOT NULL,
- project_name VARCHAR(144),
- project_id INTEGER NOT NULL,
- PRIMARY KEY (id),
- CHECK (done IN (0, 1)),
- FOREIGN KEY(account_id) REFERENCES account (id),
- FOREIGN KEY(project_id) REFERENCES project (id));
