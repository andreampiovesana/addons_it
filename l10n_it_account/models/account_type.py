# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

ACCOUNT_TYPES_NEGATIVE_SIGN = [
    "equity_unaffected",
    "equity",
    "income",
    "income_other",
    "liability_payable",
    "liability_credit_card",
    "asset_prepayments",
    "liability_current",
    "liability_non_current",
]


class AccountAccount(models.Model):
    _inherit = "account.account"

    account_balance_sign = fields.Integer(
        default=1,
        string="Balance sign",
    )

    @api.model
    def set_account_types_negative_sign(self):
        for account_type in ACCOUNT_TYPES_NEGATIVE_SIGN:
            account_ids = self.env["account.account"].search([("account_type", "=", account_type)])
            for account_id in account_ids:
                account_id.account_balance_sign = -1

    @api.constrains("account_balance_sign")
    def check_balance_sign_value(self):
        """
        Checks whether `account_balance_sign` gets a correct value of +1 or -1.
        """
        if any(t.account_balance_sign not in (-1, 1) for t in self):
            raise ValidationError(_("Balance sign's value can only be 1 or -1."))

    @api.constrains("account_balance_sign")
    def check_balance_sign_coherence(self):
        """
        Checks whether changes upon `account_balance_sign` create incoherencies
        in account groups' balance signs.
        """
        # Force check upon sign itself before checking groups signs coherence
        acc_obj = self.env["account.account"]
        key_val_dict = dict(self._fields['account_type'].selection)
        for key, val in key_val_dict.items():
            if key in ACCOUNT_TYPES_NEGATIVE_SIGN:
                sign = -1
            else:
                sign = 1
            accounts = acc_obj.search(
                [("account_type", "=", key),
                 ("account_balance_sign", "!=", sign)],
            )
            # Avoid check upon empty recordset to make it faster
            if accounts:
                raise ValidationError(_("Balance sign's not coerent"))
