Just a simple example to illustrate the issue where template fragment caching interferes with django-component media (css/js) injection middleware.
See https://github.com/django-components/django-components/issues/930.


Run

```
docker compose -f local.yml up
```

and go to `localhost:8000` in your browser. This will start up two django web workers in a docker which use a shared valkey cache.

You need to hit one worker first with your browser request, which will just happen the first time, but then the other one, which might take many refreshes and some waiting. 

You should see something like this following. Note the repeated same IP and port until we hit the second worker.

```
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41582 - "GET / HTTP/1.1" 200 OK
djc_cache_media_issue_local_django  | Internal Server Error: /
djc_cache_media_issue_local_django  | Traceback (most recent call last):
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/asgiref/sync.py", line 518, in thread_handler
djc_cache_media_issue_local_django  |     raise exc_info[1]
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django/core/handlers/exception.py", line 42, in inner
djc_cache_media_issue_local_django  |     response = await get_response(request)
djc_cache_media_issue_local_django  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django_components/dependencies.py", line 1084, in __acall__
djc_cache_media_issue_local_django  |     response = self._process_response(response)
djc_cache_media_issue_local_django  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django_components/dependencies.py", line 1091, in _process_response
djc_cache_media_issue_local_django  |     response.content = render_dependencies(response.content, type="document")
djc_cache_media_issue_local_django  |                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django_components/dependencies.py", line 502, in render_dependencies
djc_cache_media_issue_local_django  |     content_, js_dependencies, css_dependencies = _process_dep_declarations(content_, type)
djc_cache_media_issue_local_django  |                                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django_components/dependencies.py", line 654, in _process_dep_declarations
djc_cache_media_issue_local_django  |     ) = _prepare_tags_and_urls(comp_data, type)
djc_cache_media_issue_local_django  |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/site-packages/django_components/dependencies.py", line 830, in _prepare_tags_and_urls
djc_cache_media_issue_local_django  |     comp_cls = comp_hash_mapping[comp_cls_hash]
djc_cache_media_issue_local_django  |                ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^
djc_cache_media_issue_local_django  |   File "/usr/local/lib/python3.12/weakref.py", line 136, in __getitem__
djc_cache_media_issue_local_django  |     o = self.data[key]()
djc_cache_media_issue_local_django  |         ~~~~~~~~~^^^^^
djc_cache_media_issue_local_django  | KeyError: 'Icon_8b60b6'
djc_cache_media_issue_local_django  | INFO:     172.22.0.1:41594 - "GET / HTTP/1.1" 500 Internal Server Error
```