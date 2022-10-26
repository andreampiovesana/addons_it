# Copyright 2022 Openindustry.it SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import csv
import base64
import io

_logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class AccountTaxImportWizard(models.TransientModel):
    _name = "account.tax.import.wizard"

    file = fields.Binary(
        string="File",
    )
    log = fields.Text(
        string="Log",
    )

    def import_csv(self):
        at = self.env['account.tax']
        # import
        nr = 0
        file_to_import = base64.b64decode(self.file)
        data_file = io.StringIO(file_to_import.decode("utf-8"))
        data_file.seek(0)
        reader = csv.DictReader(data_file, delimiter=";")
        for row in reader:
            if not row["DESCRIPTION"] or not row["NAME"]:
                continue
            description = str(row["DESCRIPTION"])
            # exclude imported
            tax_id = at.search(
                [("description", "=", description)],
                limit=1,
            )
            if tax_id:
                continue
            # name
            name = row["NAME"]
            # use
            use = row["USE"]
            type_tax_use = 'none'
            if use == 'Vendita':
                type_tax_use = 'sale'
            if use == 'Acquisti':
                type_tax_use = 'purchase'
            # tax scope
            scope = row["SCOPE"]
            if scope == 'Beni':
                tax_scope = 'consu'
            if scope == 'Servizi':
                tax_scope = 'service'
            # amount
            amount = row["AMOUNT"].replace(',', '.')
            # amount type
            type = row["AMOUNT_TYPE"]
            if type == 'Percentuale sul prezzo':
                amount_type = 'percent'
            if type == 'Fisso':
                amount_type = 'fixed'
            # account
            account = row["ACCOUNT"]
            refund = row["REFUND"]
            # exclude
            exc_vat = row["EXC_VAT"]
            exc_ope = row["EXC_OPE"]
            exc_reg = row["EXC_REG"]
            # import
            tax_data = {
                "description": description,
                "name": name,
                "type_tax_use": type_tax_use,
                "tax_scope": tax_scope,
                "amount": float(amount),
                "amount_type": amount_type,
                "company_id": self.env.user.company_id.id,
            }
            try:
                account_id = at.with_context(tracking_disable=True).create(tax_data)
                nr += 1
                message = str(nr) + " tax " + description + " - " + name
                logging.info(message)
                print(message)
            except Exception as e:
                raise UserError(e)
            # commit
            if int(nr / 10) == nr / 10:
                self.env.cr.commit()
