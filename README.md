[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ULL36zWV)
### Estructura del projecte
```
project/
├── README.md
├── backend/                # FastAPI + MongoDB
│   ├── app.py              # Fitxer principal (tota la lògica)
│   └── requirements.txt    # Dependències
│
├── frontend/           # Interfície web
│   ├── index.html
│   ├── style.css
│   └── app.js
│
└── tests/              # Tests amb Postman
    └── Postman_API_tests.json
```
### Tutorial de funcionament ###

Primer en un sistema linux despres de actualitzar el sistema amb la comanda sudo apt install, s'haura de descarregar la seguent aplicacio.

sudo apt install python3-venv

Un cop tenim la eina per a crear environments descarregada, podrem procedir a crear el enviroment amb la seguent comanda-

sudo python3 -m venv .app

Ara que tenim el environment creat, haurem de entrar dins del environment amb la seguent comanda.

source .app/bin/activate

Un cop dins del environment, haurem de procedir en la descarrega del repositori i primer haurem de descarregar github amb la seguent comanda.

sudo apt install git

Amb git descarregat podem procedir amb la descarrega del repositori amb la seguent comanda


git clone https://github.com/llmopt2526/sprint-4-asix1-crud-de-tasques-amb-fastapi-mongodb-frontend-polcarrillo-2.git

Un cop dins del repositori haurem de instal·lar les dependencies que podem trobar al arxiu requirements.txt, pero primer haurem de descarregar pip amb la comanda

sudo apt install pip

Ara amb pip instal·lat, per a descarregar els requirements haurem de usar la seguent comanda estant dins de la carpeta on es troba el requirements

pip install -r requirements.txt

Si et dona problemes de permisos usa la seguent comanda

sudo chown -R $USER:$USER ~/.app/

Un cop tenim les dependencies descarregades, podem procedir en la execucio de la app, i per a fer-ho usarem la seguent comanda

sudo chown -R $USER:$USER ~/opt/.app/

I en aixo ja estaria



13/04/2026: Avui he acabat de posar en funcionament la api i he començat amb les comprovacions de les CRUD, ara mateix lo unic que necessito es arreglar alguns inconvenients per a les comprovacions. Un cop tingue aixo, domes em quedara crear el frontend.
