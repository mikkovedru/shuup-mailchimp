# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import datetime

from shuup import configuration
from shuup.utils.dates import to_aware
from shuup_mailchimp.configuration_keys import MC_CHECK_SUCCESS, MC_LAST_CHECK


def get_connection_info(shop):
    ts = configuration.get(shop, MC_LAST_CHECK)
    if ts:
        ts = to_aware(datetime.datetime.fromtimestamp(ts))
    return {
        "mailchimp_last_check": ts,
        "mailchimp_check_success": configuration.get(shop, MC_CHECK_SUCCESS),
    }
