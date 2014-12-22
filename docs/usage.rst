Usage
=====

``pyvat`` exposes its functionality through three simple methods:

.. module:: pyvat

.. autofunction:: check_vat_number

.. autofunction:: is_vat_number_format_valid

.. autofunction:: get_sale_vat_charge


Data types
----------

To provide the highest possible level of detail in the validation result, ``pyvat`` relies on a result object, :class:`VatNumberCheckResult` when checking VAT numbers:

.. autoclass:: VatNumberCheckResult

When determining the VAT charge for a sale, :class:`Party` is used to represent the buyer and seller and :class:`ItemType` the type of the item being sold:

.. autoclass:: Party

.. autoclass:: ItemType

The VAT charge to be applied to a sale is expressed by instances of :class:`VatCharge`:

.. autoclass:: VatCharge

.. autoclass:: VatChargeAction

   .. attribute:: charge

      Charge VAT.

   .. attribute:: reverse_charge

      No VAT charged but customer is required to account for the purchase via
      the reverse-charge mechanism.

   .. attribute:: no_charge

      No VAT charged.
