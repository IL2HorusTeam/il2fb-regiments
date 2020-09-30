Changelog
=========

* `1.1.0`_ (draft)

  API changes:

  * An instance of ``Regiments`` class must be created now to use its methods. Previously they were class methods.
  * ``verbose_name`` and ``help_text`` attributes of ``Regiment`` instances now return ``None`` instead of empty string ``""`` if their values are not found in data files.

  Data updates:

  * Data is updated to be in sync with ``IL-2 FB`` ``v4.14.1``.

  Python support:

  * Drop support of all ``Python`` versions below ``3.7``.

  Other:

  * The license is switched from ``LGPLv3`` to ``MIT``.


* `1.0.1`_ (Dec 3, 2017)

  Initial version.


.. _1.1.0: https://github.com/IL2HorusTeam/il2fb-regiments/compare/v1.0.1...v1.1.0
.. _1.0.1: https://github.com/IL2HorusTeam/il2fb-regiments/releases/tag/v1.0.1
