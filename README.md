Wazo admin ui
=============

[![Build Status](https://jenkins.wazo.community/buildStatus/icon?job=wazo-admin-ui)](https://jenkins.wazo.community/job/wazo-admin-ui)

## Translations

To extract new translations:

    % python setup.py extract_messages

To create new translation catalog:

    % python setup.py init_catalog -l <locale>

To update existing translations catalog:

    % python setup.py update_catalog

Edit file `wazo_plugind_admin_ui_group_official/translations/<locale>/LC_MESSAGES/messages.po` and compile
using:

    % python setup.py compile_catalog


## Debugging bootstrap

To enable live-edit of bootstrap.min.css, you will need to add the following line at the end of
bootstrap.min.css file:

    /*# sourceMappingURL=bootstrap.min.css.map */


Running unit tests
------------------

```
pip install tox
tox --recreate -e py3
```

Running integration tests
-------------------------

You need Docker installed.

```
cd integration_tests
pip install -U -r test-requirements.txt
make test-setup
make test
```
