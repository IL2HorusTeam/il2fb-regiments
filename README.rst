IL-2 FB Regiments
=================

This is a ``Python`` library used for accessing information about regiments present in «IL-2 Sturmovik: Forgotten Battles» flight simulator.

|pypi_package| |python_versions| |il2fb_version| |license|

|unix_build| |windows_build| |codebeat| |codacy| |scrutinizer|


Data sources
------------

Information about regiments is extracted directly from game's ``SFS`` archive named ``files.sfs``.

Data in ``il2fb/regiments/data`` directory contains the following files:

========================================= ========================== ====================
Source path in ``files.sfs``              Stored as                  Comments
========================================= ========================== ====================
``files.sfs/i18n/regShort.properties``    ``regShort_en.properties`` Added ``_en`` suffix
``files.sfs/i18n/regShort_ru.properties`` ``regShort_ru.properties``
``files.sfs/i18n/regInfo.properties``     ``regInfo_en.properties``  Added ``_en`` suffix
``files.sfs/i18n/regInfo_ru.properties``  ``regInfo_ru.properties``
``files.sfs/PaintSchemes/regiments.ini``  ``regiments.ini``
========================================= ========================== ====================

All data files retain their original encoding, which is ``CP1251``.

**Do not** edit or resave the data files in this directory manually! Instead, extract them from ``SFS`` archive and replace the current ones with them.


Installation
------------

The package is available at `PyPI <https://pypi.org/project/il2fb-regiments/>`_:

.. code-block:: shell

  pip install il2fb-regiments


Usage
-----

.. code-block:: python

  from il2fb.regiments import Regiments

  regiments = Regiments()

  regiment = regiments.get_by_code_name("USN_VT_9B")

  print(regiment.code_name)
  # USN_VT_9B

  print(regiment.air_force.verbose_name)
  # USN

  print(regiment.verbose_name)
  # VT-9 USS Essex CV-9

  print(regiment.help_text)
  # US Navy Torpedo Squadron 9 USS Essex CV-9


L10N
----

Values of human-readable properties (``verbose_name``, ``help_text``) are sensitive to the current language in use.

The current language is detected via `verboselib`_ library.

The set of supported languages is defined by ``il2fb-commons`` library.


.. code-block:: python

  from verboselib import use_language
  from il2fb.regiments import Regiments

  regiments = Regiments()

  regiment = regiments.get_by_code_name("890DBAP")

  print(regiment.verbose_name)
  # 890th "Bryansk" AP DD

  print(regiment.help_text)
  # 890th "Bryansk" AP DD

  use_language("ru")

  print(regiment.verbose_name)
  # 890-й Брянский АП ДД

  print(regiment.help_text)
  # 890-й Брянский Авиационный Полк Дальнего Действия


Serialization
-------------

It's possible to convert ``Regiment`` objects into ``Python``'s primitives for further serialization.

This can be done via ``to_primitive()`` method:

.. code-block:: python

  import json

  from il2fb.regiments import Regiments

  regiments = Regiments()

  regiment = regiments.get_by_code_name("USN_VT_9B")

  print(json.dumps(self.to_primitive(), indent=2))


Outputs:

.. code-block:: json

  {
    "air_force": {
      "name": "usn",
      "value": "un",
      "verbose_name": "USN",
      "help_text": "United States Navy",
      "country": {
        "name": "us",
        "verbose_name": "United States",
        "help_text": null
      },
      "default_flight_prefix": "UN_NN"
    },
    "code_name": "USN_VT_9B",
    "verbose_name": "VT-9 USS Essex CV-9",
    "help_text": "US Navy Torpedo Squadron 9 USS Essex CV-9"
  }


.. |unix_build| image:: https://img.shields.io/travis/IL2HorusTeam/il2fb-regiments
   :target: https://travis-ci.org/IL2HorusTeam/il2fb-regiments

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/rotwhute4uu9bin9/branch/master?svg=true
    :target: https://ci.appveyor.com/project/oblalex/il2fb-regiments
    :alt: Build status of the master branch on Windows

.. |codebeat| image:: https://codebeat.co/badges/af9c56a4-961f-4a82-9bbf-a517a36c56ee
   :target: https://codebeat.co/projects/github-com-il2horusteam-il2fb-regiments-master
   :alt: Code quality provided by «Codebeat»

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/fae50668a28b48798dd81975deb256d7
   :target: https://app.codacy.com/gh/IL2HorusTeam/il2fb-regiments
   :alt: Code quality provided by «Codacy»

.. |scrutinizer| image:: https://scrutinizer-ci.com/g/IL2HorusTeam/il2fb-regiments/badges/quality-score.png?b=master
   :target: https://scrutinizer-ci.com/g/IL2HorusTeam/il2fb-regiments/?branch=master
   :alt: Code quality provided by «Scrutinizer CI»

.. |pypi_package| image:: https://img.shields.io/pypi/v/il2fb-regiments
   :target: http://badge.fury.io/py/il2fb-regiments/
   :alt: Version of PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-3.7,3.8-brightgreen.svg
   :alt: Supported versions of Python

.. |il2fb_version| image:: https://img.shields.io/badge/IL2FB-4.14.1-blueviolet.svg
   :alt: Supported version of IL-2 FB

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/IL2HorusTeam/il2fb-regiments/blob/master/LICENSE
   :alt: MIT license

.. _verboselib: https://pypi.org/project/verboselib
