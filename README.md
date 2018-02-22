# missouri

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