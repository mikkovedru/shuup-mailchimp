# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.http.response import JsonResponse
from django.utils.translation import ugettext as _
from shuup.core.models import Shop

from shuup_mailchimp.interface import interface_test


def configurations_test(request, shop_pk):
    if not interface_test(Shop.objects.get(pk=shop_pk)):
        return JsonResponse({"message": _("Testing configuration failed")}, status=400)
    return JsonResponse({"message": _("Configuration test successful")})
