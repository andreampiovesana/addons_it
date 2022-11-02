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
                     "l10n_it_ateco.view_ateco_category_form",
                     "l10n_it_ateco.view_l10n_it_ateco_category_form",
                 ),
                 (
                     "l10n_it_ateco.view_ateco_category_tree",
                     "l10n_it_ateco.view_l10n_it_ateco_category_tree",
                 ),
                 (
                     "l10n_it_ateco.ateco_category_search",
                     "l10n_it_ateco.l10n_it_ateco_category_search",
                 ),
                 (
                     "l10n_it_ateco.action_ateco_category_search",
                     "l10n_it_ateco.action_l10n_it_ateco_category_search",
                 ),
                 (
                     "l10n_it_ateco.menu_ateco_category_form",
                     "l10n_it_ateco.menu_l10n_it_ateco_category_form",
                 ),
                 (
                     "l10n_it_ateco.access_ateco_category_user",
                     "l10n_it_ateco.access_l10n_it_ateco_category_user",
                 ),
                 (
                     "l10n_it_ateco.access_ateco_category_partner_manager",
                     "l10n_it_ateco.access_l10n_it_ateco_category_partner_manager",
                 ),
             ],
       )
       >>> openupgrade.rename_fields(
             env,
             [
                 (
                     "res.partner",
                     "res_partner",
                     "ateco_category_ids",
                     "l10n_it_ateco_category_ids",
                 ),
             ],
       )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("ateco.category", "l10n_it_ateco.category"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("ateco_category", "l10n_it_ateco_category"),
           ],
      )
      >>> env.cr.commit()
#. Riavviare Odoo
#. Aggiornare ``l10n_it_ateco``

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
                     "l10n_it_ateco.view_ateco_category_form",
                     "l10n_it_ateco.view_l10n_it_ateco_category_form",
                 ),
                 (
                     "l10n_it_ateco.view_ateco_category_tree",
                     "l10n_it_ateco.view_l10n_it_ateco_category_tree",
                 ),
                 (
                     "l10n_it_ateco.ateco_category_search",
                     "l10n_it_ateco.l10n_it_ateco_category_search",
                 ),
                 (
                     "l10n_it_ateco.action_ateco_category_search",
                     "l10n_it_ateco.action_l10n_it_ateco_category_search",
                 ),
                 (
                     "l10n_it_ateco.menu_ateco_category_form",
                     "l10n_it_ateco.menu_l10n_it_ateco_category_form",
                 ),
                 (
                     "l10n_it_ateco.access_ateco_category_user",
                     "l10n_it_ateco.access_l10n_it_ateco_category_user",
                 ),
                 (
                     "l10n_it_ateco.access_ateco_category_partner_manager",
                     "l10n_it_ateco.access_l10n_it_ateco_category_partner_manager",
                 ),
             ],
       )
       >>> openupgrade.rename_fields(
             env,
             [
                 (
                     "res.partner",
                     "res_partner",
                     "ateco_category_ids",
                     "l10n_it_ateco_category_ids",
                 ),
             ],
       )
      >>> openupgrade.rename_models(
             env.cr,
             [
                 ("ateco.category", "l10n_it_ateco.category"),
             ],
      )
      >>> openupgrade.rename_tables(
           env.cr,
           [
               ("ateco_category", "l10n_it_ateco_category"),
           ],
      )
      >>> env.cr.commit()
4. Restart Odoo
5. Update ``l10n_it_ateco`` module
