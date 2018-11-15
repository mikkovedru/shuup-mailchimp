# -*- coding: utf-8 -*-
# This file is part of Shuup Mailchimp Addon.
#
# Copyright (c) 2012-2018, Shuup Inc. All rights reserved.
#
# This source code is licensed under the OSL-3.0 license found in the
# LICENSE file in the root directory of this source tree.
import pytest
from django.db.models.signals import post_save

from shuup.core.models import CompanyContact, Order, PersonContact
from shuup.core.order_creator.signals import order_creator_finished
from shuup.testing.factories import (
    create_random_company, create_random_person, get_default_shop
)
from shuup_mailchimp.configuration_keys import (
    MC_CONTACT_SIGNAL_DISPATCH_UID, MC_ORDER_SIGNAL_DISPATCH_UID
)
from shuup_mailchimp_tests.utils import ensure_valid_configuration


@pytest.fixture()
@pytest.mark.django_db()
def default_shop():
    return get_default_shop()


@pytest.fixture()
@pytest.mark.django_db()
def valid_company():
    company = create_random_company()
    company.marketing_permission = True
    company.email = "valid@example.com"
    company.save()
    return company


@pytest.fixture()
@pytest.mark.django_db()
def valid_person():
    person = create_random_person()
    person.marketing_permission = True
    person.email = "valid@example.com"
    person.save()
    return person


@pytest.fixture()
@pytest.mark.django_db()
def valid_test_configuration():
    ensure_valid_configuration()


def pytest_configure():
    """
    For testing sake let's disconnect integration signals since
    it is quite possible that signal is not yet handled when
    checking if some update functions actually work as supposed
    """
    post_save.disconnect(sender=CompanyContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
    post_save.disconnect(sender=PersonContact, dispatch_uid=MC_CONTACT_SIGNAL_DISPATCH_UID)
    order_creator_finished.disconnect(sender=Order, dispatch_uid=MC_ORDER_SIGNAL_DISPATCH_UID)
