# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django.db import models
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumField

from shuup.core.models import Contact, Shop
from shuup.utils.analog import define_log_model


class MailchimpStatus(Enum):
    NO_STATUS = "no_status"
    SUBSCRIBED = "subscribed"
    UNSUBSCRIBED = "unsubscribed"
    CLEANED = "cleaned"
    PENDING = "pending"

    class Labels:
        NO_STATUS = _("no status")
        SUBSCRIBED = _("subscribed")
        UNSUBSCRIBED = _("unsubscribed")
        CLEANED = _("cleaned")
        PENDING = _("pending")


class MailchimpBaseModel(models.Model):
    shop = models.ForeignKey(Shop, related_name="+", on_delete=models.CASCADE, verbose_name=_("shop"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("created"))
    sent_to_mailchimp = models.DateTimeField(null=True, verbose_name=_("sent to mailchimp"))

    class Meta:
        abstract = True


class MailchimpContact(MailchimpBaseModel):
    contact = models.ForeignKey(
        Contact,
        related_name="+",
        on_delete=models.CASCADE,
        verbose_name=_("contact"),
        blank=True,
        null=True,
    )
    email = models.EmailField(max_length=254, verbose_name=_('email'), unique=True)

    class Meta:
        abstract = False


class MailchimpStatusLog(models.Model):
    email = models.EmailField(max_length=256, verbose_name=_('email'), db_index=True, help_text=_(
        "The email that will receive order confirmations and promotional materials (if permitted)."
    ))
    old_status = EnumField(MailchimpStatus, default=MailchimpStatus.NO_STATUS, max_length=12)
    new_status = EnumField(MailchimpStatus, default=MailchimpStatus.NO_STATUS, max_length=12)
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("created"))

    @classmethod
    def change_status(cls, email, new_status):
        latest = cls.objects.filter(email=email).order_by("-created").first()
        old_status = latest.new_status if latest else MailchimpStatus.NO_STATUS
        return cls.objects.create(email=email, new_status=new_status, old_status=old_status)

    @classmethod
    def latest_entry(cls, email):
        return cls.objects.filter(email=email).order_by("-created").first()


MailchimpLogEntry = define_log_model(MailchimpContact)
