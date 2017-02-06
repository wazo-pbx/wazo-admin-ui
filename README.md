Wazo admin ui
=============

[![Build Status](https://travis-ci.org/wazo-pbx/wazo-admin-ui.png?branch=master)](https://travis-ci.org/wazo-pbx/wazo-admin-ui)

## Translations

To extract new translations:

    % pybabel extract --mapping-file=wazo_admin_ui/babel.cfg --output-file=wazo_admin_ui/messages.pot .

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_admin_ui/messages.pot --output-dir=wazo_admin_ui/translations

To update existing translations catalog:

    % pybabel update --input-file=wazo_admin_ui/messages.pot --output-dir=wazo_admin_ui/translations


Edit file `wazo_admin_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % pybabel compile --directory=wazo_admin_ui/translations

