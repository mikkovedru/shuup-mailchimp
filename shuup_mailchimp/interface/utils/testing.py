# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.http.response import JsonResponse
from django.utils.translation import ugettext as _
from mailchimp3.mailchimpclient import MailChimpError
from requests import ConnectionError

from shuup import configuration
from shuup.admin.shop_provider import get_shop
from shuup.utils.dates import local_now, to_timestamp
from shuup_mailchimp.configuration_keys import MC_CHECK_SUCCESS, MC_LAST_CHECK
from shuup_mailchimp.interface.base import ShuupMailchimp


def interface_test(shop):
    client = ShuupMailchimp(shop)

    try:
        results = client.get_list()
    except (MailChimpError, ConnectionError) as e:
        return e

    status = None
    if results:
        status = results.get("status", None)
    return False if (status and status != 200) else bool(results)


def test_interface_with_response(request):
    shop = get_shop(request)
    configuration.set(shop, MC_LAST_CHECK, to_timestamp(local_now()))

    if not interface_test(shop):
        configuration.set(shop, MC_CHECK_SUCCESS, False)
        return JsonResponse({"message": _("Testing configuration failed")}, status=400)

    configuration.set(shop, MC_CHECK_SUCCESS, True)
    return JsonResponse({"message": _("Configuration test successful")})
