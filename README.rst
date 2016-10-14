IL-2 FB Regiments
=================

|pypi_package| |pypi_downloads| |python_versions| |license|

|unix_build| |windows_build| |coverage_status|

This is a Python library for accessing regiments of IL-2 Forgotten Battles
flight simulator.

Information about regiments was extracted directry from SFS archive named
``files.sfs``.

Data in ``il2fb/regiments/data`` directory contains the following files:

======================= ======================================
Filename                Original path
======================= ======================================
regShort_en.properties  files.sfs/i18n/regShort.properties
regShort_ru.properties  files.sfs/i18n/regShort_ru.properties
regInfo_en.properties   files.sfs/i18n/regInfo.properties
regInfo_ru.properties   files.sfs/i18n/regInfo_ru.properties
regiments.ini           files.sfs/PaintSchemes/regiments.ini
======================= ======================================

    **NOTE**:
        ``regShort.properties`` was renamed to ``regShort_en.properties``.
        ``regInfo.properties`` was renamed to ``regInfo_en.properties``.
        These names **must** be retained for localization sanity!

**Do not** edit or resave the contents of files in this directory manually!
Instead, extract files from ``SFS`` archive and replace current ones with them.


Usage
-----

.. code-block:: python

    from il2fb.regiments import Regiments

    regiment = Regiments.get_by_code_name("USN_VT_9B")

    print(regiment.code_name)
    # USN_VT_9B

    print(regiment.air_force.verbose_name)
    # USN

    print(regiment.verbose_name)
    # VT-9 USS Essex CV-9

    print(regiment.help_text)
    # US Navy Torpedo Squadron 9 USS Essex CV-9

Human-readable messages are sensitive to current language:

.. code-block:: python

    from verboselib import use_language
    from il2fb.regiments import Regiments

    regiment = Regiments.get_by_code_name("890DBAP")

    print(regiment.verbose_name)
    # 890th "Bryansk" AP DD

    print(regiment.help_text)
    # 890th "Bryansk" AP DD

    use_language('ru')

    print(regiment.verbose_name)
    # 890-й Брянский АП ДД

    print(regiment.help_text)
    # 890-й Брянский Авиационный Полк Дальнего Действия


.. |unix_build| image:: http://img.shields.io/travis/IL2HorusTeam/il2fb-regiments.svg?style=flat&branch=master
   :target: https://travis-ci.org/IL2HorusTeam/il2fb-regiments

.. |windows_build| image:: https://ci.appveyor.com/api/projects/status/rotwhute4uu9bin9/branch/master?svg=true
    :target: https://ci.appveyor.com/project/oblalex/il2fb-regiments
    :alt: Build status of the master branch on Windows

.. |coverage_status| image:: https://codecov.io/github/IL2HorusTeam/il2fb-regiments/coverage.svg?branch=master
   :target: https://codecov.io/github/IL2HorusTeam/il2fb-regiments?branch=master
   :alt: Test coverage

.. |pypi_package| image:: http://img.shields.io/pypi/v/il2fb-regiments.svg?style=flat
   :target: http://badge.fury.io/py/il2fb-regiments/
   :alt: Version of PyPI package

.. |pypi_downloads| image::  http://img.shields.io/pypi/dm/il2fb-regiments.svg?style=flat
   :target: https://crate.io/packages/il2fb-regiments/
   :alt: Number of downloads of PyPI package

.. |python_versions| image:: https://img.shields.io/badge/Python-2.7,3.4-brightgreen.svg?style=flat
   :alt: Supported versions of Python

.. |license| image:: https://img.shields.io/badge/license-LGPLv3-blue.svg?style=flat
   :target: https://github.com/IL2HorusTeam/il2fb-regiments/blob/master/LICENSE
   :alt: Package license
