# Copyright 2022 Openindustry.it SAS
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Import Account, Journal, Tax, Reverse Charge Type, Fiscal Position from csv",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Import Account, Journal, Tax, Reverse Charge Type, Fiscal Position from csv",
    "category": "Tools",
    "description": """
         Import Account, Journal, Tax, Reverse Charge Type, Fiscal Position from csv
    """,
    "author": "andrea.m.piovesana@gmail.com",
    "website": "https://openindustry.it",
    "depends": [
        "account",
        "l10n_it_reverse_charge",
        "l10n_it_fiscal_document_type",
        "l10n_it_fatturapa_out_rc",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/account_account.xml",
        "wizards/account_fiscpos.xml",
        "wizards/account_journal.xml",
        "wizards/account_rctype.xml",
        "wizards/account_tax.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,

}
