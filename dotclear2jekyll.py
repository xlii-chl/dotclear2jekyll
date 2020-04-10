#!/usr/bin/python3


import sys
import os
from jinja2 import Environment 
import psycopg2
from psycopg2.extras import RealDictCursor
from slugify import slugify

sql_get_posts = """
SELECT
    post_content,
    post_id,
    post_title,
    post_dt,
    post_url,
    user_id
FROM dc_post
ORDER BY post_dt ASC
;
"""

# the template variables come directly from the SQL request above
template_jekyll_post = """---
layout: post
title: "{{ post_title |e }}"
author: "{{ user_id |e }}"
redirect_from: "index.php?post/{{ post_url | slugify }} "
---

{% if post_excerpt is defined %}
{{ post_excerpt }}

<!--more-->
{% endif %}

{{ post_content }}
"""

# Fetch env variables
env_dest    = os.getenv('DEST', '.')
env_verbose = bool(os.getenv('VERBOSE', False))
env_debug   = bool(os.getenv('DEBUG', False))

try:
    # use PG env variables : PGHOST, PGDATABASE, PGUSER, etc.
    # https://www.postgresql.org/docs/current/libpq-envars.html
    connection = psycopg2.connect('')
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    # Loop over the dotclear articles
    cursor.execute(sql_get_posts)
    posts = cursor.fetchall()
    for p in posts:
        # extract the post metadata
        file_year=p['post_dt'].year;
        file_date='%d-%02d-%02d' % ( file_year, p['post_dt'].month, p['post_dt'].day)
        file_title=slugify(p['post_title'])

        # Generate the new ouput
        # replace ^M with \n
        env = Environment()
        env.filters['slugify'] = slugify
        file_content=env.from_string(template_jekyll_post).render(**p).replace('\r','\n')

        # create the year directory
        # e.g. './2004/_posts'
        file_dir=os.path.join( env_dest, str(file_year), '_posts' )
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        # write the jekyll file
        # e.g. : ./2004/_posts/2004-03-08-postgresql-weekly-news-5-janvier-2004.html
        file_path=os.path.join(file_dir,'%s-%s.md' % ( file_date,file_title) )
        with open(file_path, "w") as file_handler:
            file_handler.write(file_content)

        if env_verbose: print("Wrote %s" % file_path)

except psycopg2.Error as error :
    print ("Error while connecting to PostgreSQL", error)
except Exception as error:
    raise error
finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
