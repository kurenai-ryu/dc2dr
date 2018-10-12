===============================
dc2dr
===============================


.. image:: https://img.shields.io/pypi/v/dc2dr.svg
        :target: https://pypi.python.org/pypi/dc2dr

.. image:: https://img.shields.io/travis/alexhumphreys/dc2dr.svg
        :target: https://travis-ci.org/alexhumphreys/dc2dr

.. image:: https://readthedocs.org/projects/dc2dr/badge/?version=latest
        :target: https://dc2dr.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/alexhumphreys/dc2dr/shield.svg
     :target: https://pyup.io/repos/github/alexhumphreys/dc2dr/
     :alt: Updates


Convert Docker Compose to Docker Run Commands


* Free software: MIT license
* Documentation: https://dc2dr.readthedocs.io.


Features
--------

Takes a docker-compose file, gives back a list of docker run commands.

The supported docker-compose keys are:

  - `build`
  - `name`
  - `restart`
  - `volumes`
  - `depends_on`
  - `links`
  - `ports`
  - `expose`
  - `environment`
  - `command`
  - `image`

Usage
-----

From this dir you can run:

```
python -m dc2dr.cli tests/example-compose.yml
```

Or from in a python script:

```
from dc2dr import parser
run_commands = parser.run_commands('path/to/compose.yml')
```

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

