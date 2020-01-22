## Backend
### Tarvittavat ohjelmistot
* Python 3.6 ja yhteensopiva pip-versio. (Testattu python 3.6.8 ja pip 9.0.3). Huom. näitä ei ole välttämättä valmiina default repoissa tai asennuksessa. Ohjeita esim [täällä](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-centos-7)
* sqlite3
* git

#### Repon koodin hakeminen
```bash
git clone https://github.com/Ohtu-FaceTed/FaceTed-Backend.git
cd FaceTed-Backend
```


#### Virtual envin luonti
```python3.6 -m venv venv```. 

Ei ole välttämätön mutta vähentää riskiä että joku muu ohjelma myöhemmin hajoittaisi jotain.

#### Venvin aktivointi
```source venv/bin/activate```

Terminaalin prompt rivin alussa pitäisi olla nyt (venv).

Esim. ```(venv) [root@centos-s-1vcpu-1gb-fra1-01 FaceTed-Backend]#```.

Varmista pythonin versio ```python --version```. Pitäisi olla >= 3.6.0


#### Riippuvuuksien asennus
Hyvä asentaa ennen muita : ```pip install wheel```

Loput luetaan tiedostosta: ```pip install -r requirements.txt```


#### Tietokannan käyttäjänimen ja salasanan asetus
```vi data/user.json```

Name ja username laitetaan samoiksi. Kannattaa vaihtaa myös nimet pois administa, käyttäjällä on täydet oikeudet kannan muokkaukseen nimestä riippumatta.

#### Tietokannan alustus
```python import_data.py data app.db```

Lukee csv:t sisään kansiosta data/ ja luo app.db nimisen sqlite3 tietokannan. 

Olettaa että tietokantaa ei ole olemassa, joten jos myöhemmin haluaa lukea csv:t sisään vanha app.db pitää poistaa.


#### Avaimen luonti sessionhallintaa varten
Html-sessionhallintaa varten pitää alustaa SECRET_KEY muuttuja. 

Onnistuu ajamalla ```./generate_key.sh```./ (mahdollisesti puuttuvat ajo-oikeudet saa komennolla ```chmod u+x ./genereta_key.sh```)

Tarkista että skriptin jälkeen tiedosto secret_key.py on muotoa 

```
SECRET_KEY = b'0=A\x93}}3\xca\xcb\xbb\\\xdb(\xb3\xbc\xc7'
```


#### Palvelimen konfigurointi
Gunicornin (palvelimen) asetukset löytyy tiedostosta ```gunicorn.conf.py```

Täältä kannattaa vaihtaa ainakin muuttuja ```bind``` joka kertoo mihin osoitteeseen ja porttiin palvelin tarjoaa sisältönsä. Tässä vaiheessa voi konfiguroida mahdollisen palomuurin siten että se päästää läpi liikennettä edellä asetetusta portista.

Muuttujat capture_output ja daemon kannattaa asettaa False:ksi jos haluaa ensin varmistaa että sovellus toimii oikein. Tällöin palvelimen viestit tallentuu suoraan terminaaliin. Tiedostossa on linkki asetuksien dokumentantaation. 

Huomaa että esim. asetus nimeltä capture-output pitää kirjoittaa muodossa capture_output sillä konfiguraatio on python-tiedostossa.

Kansion luonti lokeja varten ```mkdir -p logs```


#### Palvelimen käynnistys
Sovelluksen käynnistys: ```./run.sh``` (mahdollisesti puuttuvat ajo-oikeudet saa komennolla ```chmod u+x ./run.sh```)

Kannattaa testata hakemalla endpoint /question , sillä se käyttää myös tietokantaa. Sivulla pitäisi näkyä ensimmäinen kysymys json-muodossa.

Gunicornin dokumentaatiosta löytyy tapoja miten sovelluksen saa käynnistymään itsestään, jos tälle on tarvetta.


#### Tietokannan hallintapaneeli
Endpointista /801fc3 löytyy tietokannan hallintapaneeli. Vaatii sisäänkirjautumisen. 

## Frontend

Lopuksi frontin tiedostoista fs-question.js ja fs-detail.js pitää käydä muuttamassa muuttuja const baseUrl osoittamaan uuteen osoitteeseen. Pitäisi löytyä tiedostojen alusta. 

Komponentit olettaa että ne ovat html:ssä div-tägien sisällä joiden id on faceted. Tämä sen takia että ne sitovat tähän diviin eventListenerit joiden avulla ne viestivät keskenään. Esim. toimivasti html:stä
```html
<div id="faceted">
    <fs-question.js>
    ...
</div>
```
