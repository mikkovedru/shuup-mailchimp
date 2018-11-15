# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.core.validators import validate_email, ValidationError
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shuup_mailchimp.interface import add_email_to_list


@csrf_exempt
def subscribe_newsletter(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            validate_email(email)
            add_email_to_list(request.shop, email)
            return JsonResponse({"message": "success"}, status=200)
        except ValidationError:
            return JsonResponse({"message": "error"}, status=400)
    return JsonResponse({"message": "error"}, status=400)
