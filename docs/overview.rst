Overview
========

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
HU                 Hungary               `VIES FAQ Q11`_
HR                 Croatia               `VIES FAQ Q11`_
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
SI                 Slovenia              `VIES FAQ Q11`_
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
HU                 Hungary               `VIES web service`_
HR                 Croatia               `VIES web service`_
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
SI                 Slovenia              `VIES web service`_
SK                 Slovakia              `VIES web service`_
================== ===================== ======================================

A subset of sales VAT rules are implemented for the following countries:

.. _EU electronic services: http://ec.europa.eu/taxation_customs/taxation/vat/how_vat_works/telecom/index_en.htm

================== ===================== ======================================
ISO 3166-1-alpha-2 Country               Reference
================== ===================== ======================================
AT                 Austria               `EU electronic services`_
BE                 Belgium               `EU electronic services`_
BG                 Bulgaria              `EU electronic services`_
CY                 Cyprus                `EU electronic services`_
CZ                 Czech Republic        `EU electronic services`_
DE                 Germany               `EU electronic services`_
DK                 Denmark               `EU electronic services`_
EE                 Estonia               `EU electronic services`_
EL                 Greece                `EU electronic services`_
ES                 Spain                 `EU electronic services`_
FI                 Finland               `EU electronic services`_
FR                 France                `EU electronic services`_
GB                 United Kingdom        `EU electronic services`_
HU                 Hungary               `EU electronic services`_
HR                 Croatia               `EU electronic services`_
IE                 Ireland               `EU electronic services`_
IT                 Italy                 `EU electronic services`_
LT                 Lithuania             `EU electronic services`_
LU                 Luxembourg            `EU electronic services`_
LV                 Latvia                `EU electronic services`_
MT                 Malta                 `EU electronic services`_
NL                 The Netherlands       `EU electronic services`_
PL                 Poland                `EU electronic services`_
PT                 Portugal              `EU electronic services`_
RO                 Romania               `EU electronic services`_
SE                 Sweden                `EU electronic services`_
SI                 Slovenia              `EU electronic services`_
SK                 Slovakia              `EU electronic services`_
================== ===================== ======================================
