Usage
=====

``pyvat`` exposes its functionality through two simple methods:

.. module:: pyvat

.. autofunction:: check_vat_number

.. autofunction:: is_vat_number_format_valid


Data types
----------

To provide the highest possible level of detail in the validation result, ``pyvat`` relies on a result object, :class:`VatNumberCheckResult` when checking VAT numbers:

.. autoclass:: VatNumberCheckResult
