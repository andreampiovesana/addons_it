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


class AccountFiscposImportWizard(models.TransientModel):
    _name = "account.fiscpos.import.wizard"

    file = fields.Binary(
        string="File",
    )
    log = fields.Text(
        string="Log",
    )


    def import_csv(self):
        at = self.env['account.tax']
        afp = self.env['account.fiscal.position']
        art = self.env['account.rc.type']
        # import
        nr = 0
        file_to_import = base64.b64decode(self.file)
        data_file = io.StringIO(file_to_import.decode("utf-8"))
        data_file.seek(0)
        reader = csv.DictReader(data_file, delimiter=";")
        for row in reader:
            if not row["NAME"]:
                continue
            name = row["NAME"]
            rc = row["REVERSE_CHARGE"]
            tax = row["TAX"]
            map = row["MAP_TAX"]
            # exclude imported
            fiscal_id = afp.search(
                [("name", "like", name)],
                limit=1,
            )
            if fiscal_id:
                continue
            # reverse charge
            rc_type_id = art.search(
                [('name', '=', rc)],
                limit=1,
            )
            if not rc_type_id:
                message = str(nr) + " error reverse charge " + rc
                raise UserError(message)
            # tax
            tax_id = at.search(
                [('description', '=', tax)],
                limit=1,
            )
            if not tax_id:
                message = str(nr) + " error tax " + tax
                raise UserError(message)
            # map
            map_id = at.search(
                [('description', '=', map)],
                limit=1,
            )
            if not map_id:
                message = str(nr) + " error map tax " + map
                raise UserError(message)
            # create
            map_list = []
            map_vals = {
                "tax_src_id": tax_id.id,
                "tax_dest_id": map_id.id,
            }
            map_list.append(
                (
                    0,
                    0,
                    map_vals,
                )
            )
            fiscal_data = {
                "name": name,
                "rc_type_id": rc_type_id.id,
                "tax_ids": map_list,
            }
            try:
                fiscal_id = afp.with_context(tracking_disable=True).create(fiscal_data)
                nr += 1
                message = str(nr) + " fiscal position " + name + " - " + rc + " : " + tax + " - " + map
                logging.info(message)
                print(message)
            except Exception as e:
                raise UserError(e)
            # commit
            if int(nr / 10) == nr / 10:
                self.env.cr.commit()
