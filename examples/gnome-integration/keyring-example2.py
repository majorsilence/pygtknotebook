#!/usr/bin/env python
# -*- mode: python; coding: utf-8 -*-
"""
Example showing how to store login/password in gnome keyring
"""

import gconf
import gnomekeyring
import gtk

GCONF_AUTH_KEY = "/apps/gnome-python-desktop/keyring_auth_token"

def do_something(login, password):
    print "login: %s; password: %s" % (login, password)


def get_login_password():
    keyring = gnomekeyring.get_default_keyring_sync()
    auth_token = gconf.client_get_default().get_int(GCONF_AUTH_KEY)
    if auth_token > 0:
        try:
            secret = gnomekeyring.item_get_info_sync(keyring, auth_token).get_secret()
        except gnomekeyring.DeniedError:
            login = None
            password = None
            auth_token = 0
        else:
            login, password = secret.split('\n')
    else:
        login = None
        password = None
    
    dialog = gtk.Dialog("Enter login", None, 0,
                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                         gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.props.has_separator = False
    dialog.set_default_response(gtk.RESPONSE_OK)

    hbox = gtk.HBox(False, 8)
    hbox.set_border_width(8)
    dialog.vbox.pack_start(hbox, False, False, 0)

    stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_AUTHENTICATION,
                                     gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(stock, False, False, 0)

    table = gtk.Table(2, 2)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    hbox.pack_start(table, True, True, 0)

    label = gtk.Label("_Login")
    label.set_use_underline(True)
    table.attach(label, 0, 1, 0, 1)
    local_entry1 = gtk.Entry()
    local_entry1.set_activates_default(True)
    if login is not None:
        local_entry1.set_text(login)
    table.attach(local_entry1, 1, 2, 0, 1)
    label.set_mnemonic_widget(local_entry1)

    label = gtk.Label("_Password")
    label.set_use_underline(True)
    table.attach(label, 0, 1, 1, 2)
    local_entry2 = gtk.Entry()
    local_entry2.set_visibility(False)
    local_entry2.set_activates_default(True)
    if password is not None:
        local_entry2.set_text(password)
    table.attach(local_entry2, 1, 2, 1, 2)
    label.set_mnemonic_widget(local_entry2)

    dialog.show_all()
    while 1:
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            login = local_entry1.get_text()
            password = local_entry2.get_text()
            if not login or not password:
                continue
            auth_token = gnomekeyring.item_create_sync(
                keyring,
                gnomekeyring.ITEM_GENERIC_SECRET,
                "GnomePythonDesktop keyring example, login information",
                dict(appname="GnomePythonDesktop, sync keyring example"),
                "\n".join((login, password)), True)
            gconf.client_get_default().set_int(GCONF_AUTH_KEY, auth_token)
            return login, password
        else:
            raise SystemExit

if __name__ == '__main__':
    login, password = get_login_password()
    do_something(login, password)
