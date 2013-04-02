pyvat -- VAT validation for Python
==================================

.. image:: https://travis-ci.org/iconfinder/pyvat.png?branch=master
        :target: https://travis-ci.org/iconfinder/pyvat

With EU VAT handling rules becoming ever more ridiculous and complicated, businesses within the EU are faced with the complexity of having to validate VAT numbers. ``pyvat`` was built for `Iconfinder's marketplace <http://www.iconfinder.com/>`_ to handle just this problem.

Validation of VAT numbers is performed in two steps: firstly, the VAT number is checked against an expression for the given country if one such is available, after which it is checked against a registry if one such is available.


Supported countries and registries
----------------------------------

As of the current version, ``pyvat`` has VAT number validation expressions for the following countries:

.. _VIES FAQ Q11: http://ec.europa.eu/taxation_customs/vies/faqvies.do#item_11

================== ===================== ======================================
ISO 3166-1-alpha-2 Country               Reference
================== ===================== ======================================
AT                 Austria               `VIES FAQ Q11`_
BE                 Belgium               `VIES FAQ Q11`_
BG                 Bulgaria              `VIES FAQ Q11`_
CY                 Cyprus                `VIES FAQ Q11`_
CZ                 Czech Republic        `VIES FAQ Q11`_
DE                 Germany               `VIES FAQ Q11`_
DK                 Denmark               `VIES FAQ Q11`_
EE                 Estonia               `VIES FAQ Q11`_
EL                 Greece                `VIES FAQ Q11`_
ES                 Spain                 `VIES FAQ Q11`_
FI                 Finland               `VIES FAQ Q11`_
FR                 France                `VIES FAQ Q11`_
GB                 United Kingdom        `VIES FAQ Q11`_
HU                 Hungary               `VIES FAQ Q11`_
IE                 Ireland               `VIES FAQ Q11`_
IT                 Italy                 `VIES FAQ Q11`_
LT                 Lithuania             `VIES FAQ Q11`_
LU                 Luxembourg            `VIES FAQ Q11`_
LV                 Latvia                `VIES FAQ Q11`_
MT                 Malta                 `VIES FAQ Q11`_
NL                 The Netherlands       `VIES FAQ Q11`_
PL                 Poland                `VIES FAQ Q11`_
PT                 Portugal              `VIES FAQ Q11`_
RO                 Romania               `VIES FAQ Q11`_
SE                 Sweden                `VIES FAQ Q11`_
SK                 Slovakia              `VIES FAQ Q11`_
================== ===================== ======================================

The VAT numbers for the following countries can furthermore be validated against a registry:

.. _VIES web service: http://ec.europa.eu/taxation_customs/vies/faqvies.do#item_16

================== ===================== ======================================
ISO 3166-1-alpha-2 Country               Registry
================== ===================== ======================================
AT                 Austria               `VIES web service`_
BE                 Belgium               `VIES web service`_
BG                 Bulgaria              `VIES web service`_
CY                 Cyprus                `VIES web service`_
CZ                 Czech Republic        `VIES web service`_
DE                 Germany               `VIES web service`_
DK                 Denmark               `VIES web service`_
EE                 Estonia               `VIES web service`_
EL                 Greece                `VIES web service`_
ES                 Spain                 `VIES web service`_
FI                 Finland               `VIES web service`_
FR                 France                `VIES web service`_
GB                 United Kingdom        `VIES web service`_
HU                 Hungary               `VIES web service`_
IE                 Ireland               `VIES web service`_
IT                 Italy                 `VIES web service`_
LT                 Lithuania             `VIES web service`_
LU                 Luxembourg            `VIES web service`_
LV                 Latvia                `VIES web service`_
MT                 Malta                 `VIES web service`_
NL                 The Netherlands       `VIES web service`_
PL                 Poland                `VIES web service`_
PT                 Portugal              `VIES web service`_
RO                 Romania               `VIES web service`_
SE                 Sweden                `VIES web service`_
SK                 Slovakia              `VIES web service`_
================== ===================== ======================================


Installation
------------

To install requests, do yourself a favor and don't use anything other than `pip <http://www.pip-installer.org/>`_:

.. code-block:: bash

    $ pip install pyvat


Usage
-----

``pyvat`` exposes its functionality through two simple methods:

``pyvat.is_vat_number_valid(vat_number, country_code=None)``
   Test if a VAT number is valid.
    
   If possible, the VAT number will be checked against available registries.
   
   :Parameters:
      * ``vat_number`` -- VAT number to validate.
      * ``country_code`` -- Optional country code. Should be supplied if known, as there is no guarantee that naively entered VAT numbers contain the correct alpha-2 country code prefix for EU countries just as not all non-EU countries have a reliable country code prefix. Default ``None`` prompting detection.
   
   :Returns:
      ``True`` if the VAT number can be fully asserted as valid or ``False`` if not, otherwise ``None`` indicating that the VAT number may or may not be valid.
    

``pyvat.is_vat_number_format_valid(vat_number, country_code=None)``
   Test if the format of a VAT number is valid.
   
   :Parameters:
      * ``vat_number`` -- VAT number to validate.
      * ``country_code`` -- Optional country code. Should be supplied if known, as there is no guarantee that naively entered VAT numbers contain the correct alpha-2 country code prefix for EU countries just as not all non-EU countries have a reliable country code prefix. Default ``None`` prompting detection.
   
   :Returns:
      ``True`` if the VAT number can be fully asserted as valid or ``False`` if not, otherwise ``None`` indicating that the VAT number may or may not be valid.
