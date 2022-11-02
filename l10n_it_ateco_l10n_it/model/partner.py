# Copyright (C) 2014 Abstract (<http://abstract.it>).
# Copyright (C) 2016 Ciro Urselli (<http://www.apuliasoftware.it>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):

    _inherit = "res.partner"

    l10n_it_ateco_category_ids = fields.Many2many(
        comodel_name="l10n_it_ateco.category",
        relation="ateco_category_partner_rel",
        column1="partner_id",
        column2="ateco_id",
        string="Ateco categories",
    )
