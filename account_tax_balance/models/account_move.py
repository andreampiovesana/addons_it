# Copyright 2016 Antonio Espinosa <antonio.espinosa@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _selection_financial_type(self):
        return [
            ("other", _("Other")),
            ("liquidity", _("Liquidity")),
            ("receivable", _("Receivable")),
            ("receivable_refund", _("Receivable refund")),
            ("payable", _("Payable")),
            ("payable_refund", _("Payable refund")),
        ]

    financial_type = fields.Selection(
        selection="_selection_financial_type",
        compute="_compute_financial_type",
        store=True,
        readonly=True,
    )

    @api.depends(
        "line_ids.account_id.account_type",
        "line_ids.balance",
        #"line_ids.account_id.user_type_id.type",
    )
    def _compute_financial_type(self):
        def _balance_get(line_ids, account_type):
            return sum(
                line_ids.filtered(
                    lambda x: x.account_id.account_type == account_type
                ).mapped("balance")
            )

        for move in self:
            account_types = move.line_ids.mapped("account_id.account_type")
            if "asset_cash" in account_types:
                move.financial_type = "liquidity"
            elif "payable" in account_types:
                balance = _balance_get(move.line_ids, "payable")
                move.financial_type = "payable" if balance < 0 else "payable_refund"
            elif "asset_receivable" in account_types:
                balance = _balance_get(move.line_ids, "receivable")
                move.financial_type = (
                    "receivable" if balance > 0 else "receivable_refund"
                )
            else:
                move.financial_type = "other"