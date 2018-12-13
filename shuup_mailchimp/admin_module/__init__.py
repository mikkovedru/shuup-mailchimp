# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from shuup.admin.base import AdminModule, MenuEntry
from shuup.admin.menu import ADDONS_MENU_CATEGORY
from shuup.admin.shop_provider import get_shop
from shuup.admin.utils.permissions import get_default_model_permissions
from shuup.admin.utils.urls import admin_url
from shuup.admin.views.home import SimpleHelpBlock
from shuup_mailchimp.interface import get_connection_info
from shuup_mailchimp.models import MailchimpContact


class MailchimpAdminModule(AdminModule):
    name = _("Mailchimp")

    def get_urls(self):
        return [
            admin_url(
                "^mailchimp/connect/$",
                "shuup_mailchimp.admin_module.views.MailchimpConnectView",
                name="mailchimp.connect",
                permissions=get_default_model_permissions(MailchimpContact),
            ),
        ]

    def get_menu_entries(self, request):
        return [
            MenuEntry(
                text=self.name,
                icon="fa fa-mail",
                url="shuup_admin:mailchimp.connect",
                category=ADDONS_MENU_CATEGORY
            )
        ]

    def get_required_permissions(self):
        return get_default_model_permissions(MailchimpContact)

    def get_help_blocks(self, request, kind):
        if kind != "setup":
            return

        shop = get_shop(request)
        connection_info = get_connection_info(shop)
        last_check_success = connection_info.get("check_success", False)
        connected = (connection_info.get("last_check") and last_check_success)

        if kind == "setup":
            actions = [
                {
                    "text": _("Re-connect Mailchimp") if connected else _("Connect Mailchimp"),
                    "url": reverse_lazy("shuup_admin:mailchimp.connect"),
                }
            ]

            yield SimpleHelpBlock(
                priority=0.1,  # not the first but pretty high...
                text=_("MailChimp"),
                description_html=True,
                description=_("Connect your Mailchimp account to Shuup store. "
                              "Once connected, your customers can be added to your mailing list."),
                actions=actions,
                icon_url="shuup_mailchimp/Mailchimp_Logo-Vertical_Black.png",
                done=connected,
            )
