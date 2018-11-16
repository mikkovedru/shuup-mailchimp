# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

import requests
from mailchimp3 import MailChimp

from shuup_mailchimp.interface.member import ShuupMember

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class ShuupMailchimpClient(MailChimp):
    """
    mailchimp3.Mailchimp with extended ShuupMember functionality
    """
    def __init__(self, *args, **kwargs):
        super(ShuupMailchimpClient, self).__init__(*args, **kwargs)
        self.shuup_member = ShuupMember(self)

    def _put(self, url, data=None):
        """
        Handle PUT request.

        .. note::

           There already is a `_put` method in the base class in
           mailchimp3 1.0.17, but 1.0.12 doesn't have it and that's
           currently the latest version supporting Python 3.
        """
        url = urljoin(self.base_url, url)
        r = requests.put(url, auth=self.auth, json=data)
        return r.json()
