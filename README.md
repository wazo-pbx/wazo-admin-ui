Wazo admin ui
=============

## Translations

To extract new translations:

    % python setup.py extract_messages

To create new translation catalog:

    % python setup.py init_catalog -l <locale>

To update existing translations catalog:

    % python setup.py update_catalog

Edit file `wazo_admin_ui/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % python setup.py compile_catalog
