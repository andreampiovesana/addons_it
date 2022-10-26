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


class AccountRCTypeImportWizard(models.TransientModel):
    _name = "account.rctype.import.wizard"

    file = fields.Binary(
        string="File",
    )
    log = fields.Text(
        string="Log",
    )

    def import_csv(self):
        rp = self.env['res.partner']
        art = self.env['account.rc.type']
        fdt = self.env['fiscal.document.type']
        aa = self.env['account.account']
        aj = self.env['account.journal']
        at = self.env['account.tax']
        # import
        nr = 0
        file_to_import = base64.b64decode(self.file)
        data_file = io.StringIO(file_to_import.decode("utf-8"))
        data_file.seek(0)
        reader = csv.DictReader(data_file, delimiter=";")
        for row in reader:
            if not row["NAME"] or not row["DESCRIPTION"]:
                continue
            name = row["NAME"]
            description = str(row["DESCRIPTION"])
            method = row["METHOD"]
            fiscal_type = row["FISCAL_DOC"]
            partner_type = row["PARTNER_TYPE"]
            partner_rc = row["PARTNER_RC"]
            journal_rc = row["JOURNAL_RC"]
            journal_pay_rc = row["JOURNAL_PAY_RC"]
            account_rc = str(row["ACCOUNT_RC"])
            tax_original = str(row["TAX_ORIGINAL"])
            tax_purchase = str(row["TAX_PURCHASE"])
            tax_sale = str(row["TAX_SALE"])
            # exclude imported
            rc_type_id = art.search(
                [("name", "like", name)],
                limit=1,
            )
            if rc_type_id:
                continue
            # fiscal document type
            fis_type_id = fdt.search(
                [('code', '=', fiscal_type)],
                limit=1,
            )
            if not fis_type_id:
                message = str(nr) + " error fiscal document type " + fiscal_type
                raise UserError(message)
            # partner rc
            partner_id = rp.search(
                [('name', '=', partner_rc)],
                limit=1,
            )
            if not partner_id:
                message = str(nr) + " error partner reverse charge " + partner_rc
                #raise UserError(message)
                partner_id = self.env.user.company_id.partner_id
            # journal rc
            journal_id = aj.search(
                [('code', '=', journal_rc)],
                limit=1,
            )
            if not journal_id:
                message = str(nr) + " error journal reverse charge " + journal_rc
                raise UserError(message)
            # journal payment rc
            journal_pay_id = aj.search(
                [('code', '=', journal_pay_rc)],
                limit=1,
            )
            if not journal_pay_id:
                message = str(nr) + " error journal payment reverse charge " + journal_pay_rc
                raise UserError(message)
            # account rc
            account_id = aa.search(
                [('code', '=', account_rc)],
                limit=1,
            )
            if not account_id:
                message = str(nr) + " error account reverse charge " + account_rc
                raise UserError(message)
            # original tax
            original_tax_id = at.search(
                [('description', '=', tax_original)],
                limit=1,
            )
            if not original_tax_id:
                message = str(nr) + " error original tax " + tax_original
                raise UserError(message)
            # purchase tax
            purchase_tax_id = at.search(
                [('description', '=', tax_purchase)],
                limit=1,
            )
            if not purchase_tax_id:
                message = str(nr) + " error purchase tax " + tax_purchase
                raise UserError(message)
            # sale tax
            sale_tax_id = at.search(
                [('description', '=', tax_sale)],
                limit=1,
            )
            if not sale_tax_id:
                message = str(nr) + " error sale tax " + tax_sale
                raise UserError(message)
            # map
            map_list = []
            map_vals = {
                #"original_tax_id": original_tax_id.id,
                "purchase_tax_id": purchase_tax_id.id,
                "sale_tax_id": sale_tax_id.id,
            }
            map_list.append(
                (
                    0,
                    0,
                    map_vals,
                )
            )

            # import
            rc_type_data = {
                "name": name,
                "method": method,
                "e_invoice_suppliers": False,
                "description": description,
                "fiscal_document_type_id": fis_type_id.id,
                "company_id": self.env.user.company_id.id,
                "partner_type": partner_type,
                "with_supplier_self_invoice": False,
                "partner_id": partner_id.id,
                "journal_id": journal_id.id,
                "payment_journal_id": journal_pay_id.id,
                "transitory_account_id": account_id.id,
                "tax_ids": map_list,
            }
            try:
                rctype_id = art.with_context(tracking_disable=True).create(rc_type_data)
                nr += 1
                message = str(nr) + " reverse charge type " + name + " - " + description
                logging.info(message)
                print(message)
            except Exception as e:
                raise UserError(e)
            # commit
            if int(nr / 10) == nr / 10:
                self.env.cr.commit()
