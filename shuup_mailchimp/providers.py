# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from django import forms
from django.utils.translation import ugettext

from shuup.front.providers import FormFieldDefinition, FormFieldProvider


class MailchimpFieldProvider(FormFieldProvider):
    error_message = ""

    def get_fields(self, **kwargs):
        fields = []
        field = forms.BooleanField(
            label=ugettext("I want to receive marketing material"),
            required=False,
            error_messages=dict(required=self.error_message)
        )
        definition = FormFieldDefinition(name="accept_mailchimp", field=field)
        fields.append(definition)
        return fields
