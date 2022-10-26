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


class AccountJournalImportWizard(models.TransientModel):
    _name = "account.journal.import.wizard"

    file = fields.Binary(
        string="File",
    )
    log = fields.Text(
        string="Log",
    )


    def import_csv(self):
        aa = self.env['account.account']
        aj = self.env['account.journal']
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
            acc = row["DEFAULT_ACCOUNT"]
            # debi = row["DEFAULT_DEBIT"]
            # cred = row["DEFAULT_CREDIT"]
            # exclude imported
            journal_id = aj.search(
                [("code", "like", code)],
                limit=1,
            )
            if journal_id:
                continue
            # # default debit account
            # debi_id = aa.search(
            #     [('code', '=', debi)],
            #     limit=1,
            # )
            # if not debi_id:
            #     message = str(nr) + " error debit account " + cred
            #     raise UserError(message)
            # # default credit account
            # cred_id = aa.search(
            #     [('code', '=', cred)],
            #     limit=1,
            # )
            # if not cred_id:
            #     message = str(nr) + " error credit account " + cred
            #     raise UserError(message)
            # default account
            account_id = aa.search(
                [('code', '=', acc)],
                limit=1,
            )
            if not account_id:
                message = str(nr) + " error account " + acc
                raise UserError(message)
            # type
            STYPE = ['sale', 'purchase', 'cash', 'bank', 'general']
            TTYPE = ['Vendita', 'Acquisto', 'Cassa', 'Banca', 'Varie']
            i = TTYPE.index(type)
            if type not in TTYPE:
                message = str(nr) + " error journal type " + type
                raise UserError(message)
            # create
            journal_data = {
                "code": code,
                "name": name,
                "type": STYPE[i],
                "default_account_id": account_id.id,
                # "default_debit_account_id": debi_id.id,
                # "default_credit_account_id": cred_id.id,
            }
            try:
                journal_id = aj.with_context(tracking_disable=True).create(journal_data)
                nr += 1
                message = str(nr) + " journal " + code + " - " + name
                logging.info(message)
                print(message)
            except Exception as e:
                raise UserError(e)
            # commit
            if int(nr / 10) == nr / 10:
                self.env.cr.commit()
