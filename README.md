Wazo admin ui
=============

[![Build Status](https://travis-ci.org/wazo-pbx/wazo-admin-ui.png?branch=master)](https://travis-ci.org/wazo-pbx/wazo-admin-ui)

## Translations

To extract new translations:

    % pybabel extract --mapping=wazo_admin_ui/translations/babel.cfg -k l_ -k lazy_gettext --output=wazo_admin_ui/translations/messages.pot wazo_admin_ui/

To create new translation catalog:

    % pybabel init -l <locale> --input-file=wazo_admin_ui/translations/messages.pot --output-dir=wazo_admin_ui/translations

To update existing translations catalog:

    % pybabel update --input-file=wazo_admin_ui/translations/messages.pot --output-dir=wazo_admin_ui/translations


Edit file `wazo_admin_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % pybabel compile --directory=wazo_admin_ui/translations


## Debugging bootstrap

To enable live-edit of bootstrap.min.css, you will need to add the following line at the end of
bootstrap.min.css file:

    /*# sourceMappingURL=bootstrap.min.css.map */


## Integration tests

### Environment variables

* VIRTUAL_DISPLAY=0: do not show the window containing the testing browser
