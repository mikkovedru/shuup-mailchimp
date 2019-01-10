# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2019, Shoop Commerce Ltd. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from shuup import configuration
from shuup.testing.factories import get_default_shop
from shuup_mailchimp.configuration_keys import MC_API, MC_LIST_ID, MC_USERNAME

MC_API_KEY = "1337eab647efd2e0de577de67e0ce754-us2"
MC_API_USERNAME = "some-username"
MC_API_LIST_ID = "1337ba85a0"


def ensure_valid_configuration():
    configuration.cache.clear()
    shop = get_default_shop()
    configuration.set(shop, MC_API, MC_API_KEY)
    configuration.set(shop, MC_USERNAME, MC_API_USERNAME)
    configuration.set(shop, MC_LIST_ID, MC_API_LIST_ID)
