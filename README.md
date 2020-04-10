# dotclear2jekyll

Quick and Dirty migration script from dotclear to jekyll

## Install

```bash
$ git clone git@github.com:postgresqlfr/dotclear2jekyll.git
$ pip install -r requirements
```

## Usage


```bash
$ PGHOST=localhost
$ PGDATABASE=dotclear
$ PGUSER=bob
$ PGPASSWORD=SeCReT
$ DEST=/tmp/foo
$ VERBOSE=true
$ ./dotclear2jekyll.py
```
