# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import six
from django.views.generic import FormView

from shuup import configuration
from shuup.admin.shop_provider import get_shop
from shuup_mailchimp.admin_module.forms import (
    ConfigurationForm, FORM_FIELD_TO_CONF_KEY_MAP
)
from shuup_mailchimp.interface.utils.connection import get_connection_info
from shuup_mailchimp.interface.utils.testing import (
    test_interface_with_response
)


class MailchimpConnectView(FormView):
    template_name = "shuup_mailchimp/admin/connect.jinja"
    form_class = ConfigurationForm

    def get_form_kwargs(self):
        kwargs = super(MailchimpConnectView, self).get_form_kwargs()
        kwargs["shop"] = get_shop(self.request)
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super(MailchimpConnectView, self).get_context_data(**kwargs)
        shop = get_shop(self.request)
        ctx["shop"] = shop
        for key, value in six.iteritems(get_connection_info(shop)):
            ctx[key] = value
        return ctx

    def post(self, request, *args, **kwargs):
        data = request.POST
        shop = get_shop(request)
        for form_field, conf_key in six.iteritems(FORM_FIELD_TO_CONF_KEY_MAP):
            configuration.set(shop, conf_key, data.get(form_field))
        return test_interface_with_response(request)
