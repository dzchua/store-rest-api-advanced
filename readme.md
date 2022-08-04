# Advanced Store REST api

Built upon previous store REST api with Marshmallow:
https://flask-marshmallow.readthedocs.io/en/latest/


## Flask-Marshmallow
Used to defined the schemas. 
 
## E-mail confirmation
Registration of users have to be confirmed through e-mail and it is done using MailGun.

## Posting image
Every image is posted to file directory static/images/user_id, same functionality as others such as to post, get and delete from the designated directory.
