# missouri

USS Missouri (BB-63) ("Mighty Mo" or "Big Mo") is a United States Navy Iowa-class battleship and was the third ship of the U.S. Navy to be named after the U.S. state of Missouri. Missouri was the last battleship commissioned by the United States and is best remembered as the site of the surrender of the Empire of Japan which ended World War II.

## Install virtualenv

## Import essential environment variables

```shell
export MAIL_USERNAME=<your email@example.com>
export MAIL_PASSWORD=<your smtp service pasword>
export MISSOURI_ADMIN=<administrator email account>
```

## Install database migration

Use `init` command to create database migraion

```shell
python missouri.py init
```

Use `migrate` command to generate migration script automatically

```shell
python missouri.py migrate -m "initial migration"
```

Upgrade database. It will create a new database if use it for the first time.

```shell
python missouri.py db upgrade
```

## Deploy your blog

```shell
python missouri.py db deploy
```

## Local Debugging

Run command as below and open [http://localhost:9000/](http://localhost:9000/) in your brower:

```shell
python missouri.py run server
```
