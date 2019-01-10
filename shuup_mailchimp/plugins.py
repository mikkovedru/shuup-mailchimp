# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from shuup.core.shop_provider import get_shop
from shuup.xtheme import TemplatedPlugin
from shuup.xtheme.plugins.forms import TranslatableField
from shuup.xtheme.resources import add_resource
from shuup_mailchimp.interface import get_connection_info


class NewsletterPlugin(TemplatedPlugin):
    identifier = "shuup_mailchimp.newsletter"
    name = _("Subscribe Newsletter (Mailchimp)")
    template_name = "shuup_mailchimp/newsletter.jinja"

    fields = [
        ("title", TranslatableField(label=_("Title"), required=True, initial="")),
        ("lead", TranslatableField(label=_("Lead text"), required=True, initial="")),
        ("link_title", TranslatableField(label=_("Submit button text"), required=True, initial="")),
        ("input_placeholder_text", TranslatableField(label=_("Input placeholder text"), required=True, initial="")),
        ("success_message", TranslatableField(label=_("Success message"), required=True, initial="")),
        ("error_message", TranslatableField(label=_("Error message"), required=True, initial="")),
    ]

    def render(self, context):
        """
        Custom render for to add css resource for carousel
        :param context: current context
        :return: html content for the plugin
        """
        add_resource(context, "head_end", "%sshuup_mailchimp/css/style.css" % settings.STATIC_URL)
        add_resource(context, "body_end", "%sshuup_mailchimp/js/script.js" % settings.STATIC_URL)
        return super(NewsletterPlugin, self).render(context)

    def get_context_data(self, context):
        shop = get_shop(context["request"])
        cfg = get_connection_info(shop)
        return {
            "mailchimp_enabled": cfg.get("mailchimp_check_success", False),
            "title": self.get_translated_value("title"),
            "lead": self.get_translated_value("lead"),
            "link_title": self.get_translated_value("link_title"),
            "input_placeholder_text": self.get_translated_value("input_placeholder_text"),
            "success_message": self.get_translated_value("success_message"),
            "error_message": self.get_translated_value("error_message"),
        }
