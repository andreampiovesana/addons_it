**Italiano**

Necessario eseguire la seguente procedura per rinomina col prefisso ``l10n_it_``.

#. Installare ``openupgradelib``:

   .. code::

      pip3 install git+https://github.com/OCA/openupgradelib.git@master
#. Lanciare Odoo con il paramentro ``shell``
#. Eseguire i seguenti comandi:

   .. code::

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "l10n_it_abicab.view_bank_filter_abicab",
                     "l10n_it_abicab.view_bank_filter_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_bank_tree_abicab",
                     "l10n_it_abicab.view_bank_tree_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_bank_form_abicab",
                     "l10n_it_abicab.view_bank_form_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_partner_bank_form_abicab_form",
                     "l10n_it_abicab.view_partner_bank_form_l10n_it_abicab_form",
                 ),
             ],
       )
       >>> openupgrade.rename_fields(
             env,
             [
                 (
                     "res.bank",
                     "res_bank",
                     "abi",
                     "l10n_it_abi",
                 ),
                 (
                     "res.bank",
                     "res_bank",
                     "cab",
                     "l10n_it_cab",
                 ),
                 (
                     "res.partner.bank",
                     "res_partner_bank",
                     "bank_abi",
                     "l10n_it_bank_abi",
                 ),
                 (
                     "res.partner.bank",
                     "res_partner_bank",
                     "bank_cab",
                     "l10n_it_bank_cab",
                 ),
             ],
       )
      >>> env.cr.commit()
#. Riavviare Odoo
#. Aggiornare ``l10n_it_abicab``

**English**

You need to follow the following steps for renaming with prefix ``l10n_it_``.

1. Install ``openupgradelib``:

   .. code::

       pip3 install git+https://github.com/OCA/openupgradelib.git@master
2. Run Odoo with the ``shell`` command
3. Execute the following commands:

   .. code::

       >>> from openupgradelib import openupgrade
       >>> openupgrade.rename_xmlids(
             env.cr,
             [
                 (
                     "l10n_it_abicab.view_bank_filter_abicab",
                     "l10n_it_abicab.view_bank_filter_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_bank_tree_abicab",
                     "l10n_it_abicab.view_bank_tree_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_bank_form_abicab",
                     "l10n_it_abicab.view_bank_form_l10n_it_abicab",
                 ),
                 (
                     "l10n_it_abicab.view_partner_bank_form_abicab_form",
                     "l10n_it_abicab.view_partner_bank_form_l10n_it_abicab_form",
                 ),
             ],
       )
       >>> openupgrade.rename_fields(
             env,
             [
                 (
                     "res.bank",
                     "res_bank",
                     "abi",
                     "l10n_it_abi",
                 ),
                 (
                     "res.bank",
                     "res_bank",
                     "cab",
                     "l10n_it_cab",
                 ),
                 (
                     "res.partner.bank",
                     "res_partner_bank",
                     "bank_abi",
                     "l10n_it_bank_abi",
                 ),
                 (
                     "res.partner.bank",
                     "res_partner_bank",
                     "bank_cab",
                     "l10n_it_bank_cab",
                 ),
             ],
       )
      >>> env.cr.commit()
4. Restart Odoo
5. Update ``l10n_it_abicab`` module
