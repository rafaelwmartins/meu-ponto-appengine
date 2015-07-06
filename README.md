Meu Ponto App Engine
====================
This repository contains the code necessary to serve the static assets (HTML, CSS, JavaScript, etc) and the *register* end point of [Meu Ponto] on [Google App Engine].

Register
--------
In order to add or modify a record, you can call the *register* end point. The following example registers *13:02* as the *Entry 2* of *2015-07-06* for user *123*:

```bash
curl -X POST -d user=123 -d token=456 -d year=2015 -d month=07 -d day=06 -d entry=2 -d value=13:02 http://meu-ponto.appspot.com/register
```

`user` and `token` are available inside the configuration screen of the app.

For `entry`, the following arguments are accepted:

- **0**: Entry 1
- **1**: Exit 1
- **2**: Entry 2
- **3**: Exit 2

License
-------
Meu Ponto App Engine is freely distributable under the terms of the MIT license.

[Meu Ponto]: https://github.com/rafaelwmartins/meu-ponto
[Google App Engine]: https://appengine.google.com
