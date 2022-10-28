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


class AccountAccountImportWizard(models.TransientModel):
    _name = "account.account.import.wizard"

    file = fields.Binary(
        string="File",
    )
    log = fields.Text(
        string="Log",
    )

    def import_csv(self):
        aa = self.env['account.account']
        # import
        nr = 0
        file_to_import = base64.b64decode(self.file)
        data_file = io.StringIO(file_to_import.decode("utf-8"))
        data_file.seek(0)
        reader = csv.DictReader(data_file, delimiter=";")
        for row in reader:
            if not row["CODE"] or not row["NAME"]:
                continue
            code = str(row["CODE"])
            name = row["NAME"]
            type = row["TYPE"]
            reco = row["RECONCILE"]
            intt = row["INTERNAL_TYPE"]
            intg = row["INTERNAL_GROUP"]
            # exclude imported
            account_id = aa.search(
                [("code", "like", code)],
                limit=1,
            )
            if account_id:
                continue
            # import
            account_data = {
                "code": code,
                "name": name,
                "account_type": type,
                "reconcile": reco,
                "internal_type": intt,
                "internal_group": intg,
            }
            try:
                account_id = aa.with_context(tracking_disable=True).create(account_data)
                nr += 1
                message = str(nr) + " account " + code + " - " + name
                logging.info(message)
                print(message)
            except Exception as e:
                raise UserError(e)
            # commit
            if int(nr / 10) == nr / 10:
                self.env.cr.commit()
