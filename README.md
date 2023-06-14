# ***TRANSPORTDOCS***

TRANSPORTDOCS project consist from two apps:

- *Control app*
- *Business app*

Both app is developed on [FastAPI](https://fastapi.tiangolo.com/)

Because this is a small project I`m using local databases *sqlite* for both apps.

## *Control app* this app oriented on control organization such as Police etc.

Control app has two types of user role:

- admin
- controller

Admin user it is main user who can do all administration functionality such as:

- create, read, update, delete orgazination
- create, read, update, delete department
- create, read, update, delete controller user

Controller user it is user who can do only one things:

- check transport document

If controller user check document and document parameter such as height, length, width was changed after appling signes, controller user get message response about invalid this document. And controll organization can make investigation about companies and this cargo.

In other case if all Ok controller get as response all information about document such as time created document, cargo parameters, signes sender and receiver companies.

To get information about document, controller send API request to another app - Business app (manage app).

## *Business app* this app oriented on commercial companies who transport cargo.

Business app provides commercial relations between companies that deliver goods.

Functionality of the Business app:

- registration user(company owner)
- create, read, update, delete companies
- create, read, update, delete transport document
- appling signe on document

**Both app database separated from each other.**

## Install TRANSPORTDOCS

> git clone git@github.com:RomanVitiuk/TransportDocs.git
> cd '*project_folder*'

Make your controlle_app/.env and manage_app/.env files by example of controlle_app/env-example and manage_app/env-example files.

**To run project from Docker, first of all check your ip docker.**

On unix this can do with command:

> ip a

If you docker ip match **172.17.0.1**, run:

> docker compose up
or
> docker compose up -d

If it`s not, change ip address in request url in file *controle_app/services/check_docs_service.py* on your docker ip and run:

> docker compose up
or
> docker compose up -d

**To run project from terminal:**

Uncomment variable response under localhost ip in file *controle_app/services/check_docs_service.py*.
Comment variable response under docker ip in file *controle_app/services/check_docs_service.py*.

start Controll App

> cd '*project_folder*'
> cd control_app/ && uvicorn main:app -p 8001

start Business App

> cd '*project_folder*'
> cd manage_app/ && uvicorn main:app -p 8002
