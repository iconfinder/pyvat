class VatNumberCheckResult(object):
    """Result of a VAT number validation check.

    :ivar is_valid:
        Boolean value indicating if the checked VAT number was deemed to be
        valid. ``True`` if the VAT number is valid, ``False`` if the VAT
        number is positively invalid or ``None`` if the validity is
        nondeterministic due to adverse conditions.
    :ivar log_lines:
        Check log lines.
    """

    def __init__(self, is_valid=None, log_lines=None):
        self.is_valid = is_valid
        self.log_lines = log_lines or []
