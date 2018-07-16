# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.conf.urls import patterns, url

from shuup_mailchimp.views import subscribe_newsletter

urlpatterns = patterns(
    '',
    url(r'^subscribe/$', subscribe_newsletter, name='subscribe_newsletter'),
)
