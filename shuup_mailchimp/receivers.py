# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.dispatch import receiver

from shuup.front.signals import person_registration_save
from shuup_mailchimp.interface import add_email_to_list


@receiver(person_registration_save)
def update_mailchimp_contact(sender, request, user, contact, *args, **kwargs):
    if request.POST.get("accept_mailchimp", "off") == "off":
        return
    for shop in contact.shops.all():
        add_email_to_list(shop, contact.email, contact=contact)
    contact.marketing_permission = True
    contact.save()
