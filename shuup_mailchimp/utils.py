# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
from shuup_mailchimp.models import MailchimpStatus, MailchimpStatusLog


def added_to_mailchimp(email):
    latest_log = MailchimpStatusLog.latest_entry(email)
    return (latest_log and latest_log.new_status == MailchimpStatus.SUBSCRIBED)
