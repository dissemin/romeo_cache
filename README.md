# romeo_cache
A simple mirror for the SHERPA/RoMEO API, written with Django.

Reference page for the API:
http://www.sherpa.ac.uk/romeo/api.html

Usage
-----

- hook the application to a Web server:
  https://docs.djangoproject.com/en/1.8/howto/deployment/
- use the proxy as if you were using the original API, changing the base URL to:
  http://myproxy.com/romeo/api29.php
  (the original relative URL has been kept, although we do not use PHP)
  
Why a mirror
------------

The SHERPA server times out, returns 500 errors… And very often we perform the same queries!
So let's cache the responses and serve them faster.
