# kozzy-backend

This is the Backend Production Repository for the Kozzy web application.

## Table of Contents
- [Running the API in docker compose](#running-the-api-in-docker)
- [Code Style Verification with Pycodestyle](#code-style-verification-with-pycodestyle)

## Running the API in docker compose

To run the API in docker follow these steps:

### Step 1:

you need to run this comand at the root of the directory:
```bash
docker compose up --build
```
If you run into issues installing Docker and Docker Compose, I found the third answer in this [Stack Overflow thread](https://stackoverflow.com/questions/78688526/docker-compose-is-not-a-docker-command-ubuntu-24-04-lts) very useful.


### Step 2:

The command on step 1 also creates a mongodb container,
and we need to get into the mongodb container and set it up using these commands in another terminal:
```bash
# access the container
docker exec -it mongo_container /bin/bash

# from inside the container access the mongo db
mongosh

# move into the admin data base and create the new user and password
use admin

db.createUser({
  user: "kozzydb",
  pwd: "Me@kozzy247",
  roles: [ { role: "root", db: "admin" } ]
})

# then exit the mongo shell
exit

# then exit the container shell
exit
```
now you can start testing your endpoints at the local host port 5000.
You can also stop the containers using ctrl+c then to restart them use:

```bash
docker start kozzy-backend-api-1
docker start mongo_container
```

## Code Style Verification with Pycodestyle

To verify your code meets the coding standard before you commit, follow these steps:

### Step 1:

Use pycodestyle to check the following folders before commit for any style issues example:

```bash
pycodestyle web_flask/
pycodestyle views/
pycodestyle models/
pycodestyle models/engines/
```
## Important Notes

These are the various folders and what they are used for:
* [Models](models): All models to be saved here
* [Engines](models/engines/): scripts to interact with database are saved here
* [Views](views): All endpoints to be saved here
* [Web Flask](web_flask): Houses the main flask server code.

To run the code, ensure you create a .env file at the root of the project folder and use the example.env file as a reference to what should be contained within your .env file, making sure the password and username is exactly what is contained in your create user command above.
** **

Once you are up and running locally, you can find the API swagger Docs at the link: http://127.0.0.1:5000/apidocs/
