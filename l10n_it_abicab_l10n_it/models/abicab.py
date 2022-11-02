# Copyright 2015 Associazione Odoo Italia (<http://www.odoo-italia.org>)
# Copyright 2016 Davide Corio (Abstract)
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ResBank(models.Model):

    _inherit = "res.bank"

    l10n_it_abi = fields.Char(size=5, string="ABI")
    l10n_it_cab = fields.Char(size=5, string="CAB")


class ResPartnerBank(models.Model):

    _inherit = "res.partner.bank"

    l10n_it_bank_abi = fields.Char(
        size=5, string="ABI", related="bank_id.l10n_it_abi", store=True
    )
    l10n_it_bank_cab = fields.Char(
        size=5, string="CAB", related="bank_id.l10n_it_cab", store=True
    )

    @api.onchange("bank_id")
    def onchange_bank_id(self):
        if self.bank_id:
            self.l10n_it_bank_abi = self.bank_id.l10n_it_abi
            self.l10n_it_bank_cab = self.bank_id.l10n_it_cab
