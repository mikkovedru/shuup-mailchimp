import json

import pytest
from django.utils.encoding import force_text

from shuup import configuration
from shuup.admin.views.home import HomeView
from shuup.testing.utils import apply_request_middleware
from shuup_mailchimp.admin_module.forms import ConfigurationForm
from shuup_mailchimp.admin_module.views import MailchimpConnectView
from shuup_mailchimp.configuration_keys import MC_API, MC_LIST_ID, MC_USERNAME
from shuup_mailchimp_tests.utils import (
    ensure_valid_configuration, MC_API_KEY, MC_API_LIST_ID, MC_API_USERNAME
)


@pytest.mark.django_db
def test_connect_view(rf, admin_user, default_shop):
    view = MailchimpConnectView.as_view()
    request = apply_request_middleware(rf.get("/"), user=admin_user, shop=default_shop)
    response = view(request)
    assert response.status_code == 200
    response.render()

    content = force_text(response.content)
    assert "Save and Test Connection" in content

    ensure_valid_configuration()

    response = view(request)
    assert response.status_code == 200
    response.render()

    content = force_text(response.content)
    assert configuration.get(default_shop, MC_API) in content
    assert configuration.get(default_shop, MC_USERNAME) in content
    assert configuration.get(default_shop, MC_LIST_ID) in content


@pytest.mark.django_db
def test_connect_view_with_post(rf, admin_user, default_shop):
    configuration.cache.clear()
    view = MailchimpConnectView.as_view()
    request = apply_request_middleware(rf.get("/"), user=admin_user, shop=default_shop)
    response = view(request)
    assert response.status_code == 200
    response.render()

    content = force_text(response.content)
    assert "Save and Test Connection" in content

    request = apply_request_middleware(rf.post("/", data={
        "api_key": MC_API_KEY,
        "list_id": MC_API_LIST_ID,
        "username": MC_API_USERNAME,
    }), user=admin_user, shop=default_shop)

    response = view(request)
    assert response.status_code == 200
    response_data = json.loads(response.content.decode("utf-8"))
    assert response_data.get("message")

    request = apply_request_middleware(rf.get("/"), user=admin_user, shop=default_shop)
    response = view(request)
    assert response.status_code == 200
    response.render()
    content = force_text(response.content)
    configuration.cache.clear()
    assert configuration.get(default_shop, MC_API) in content
    assert configuration.get(default_shop, MC_USERNAME) in content
    assert configuration.get(default_shop, MC_LIST_ID) in content


@pytest.mark.django_db
def test_home_view(rf, admin_user, default_shop):
    request = apply_request_middleware(rf.get("/"), user=admin_user, shop=default_shop)
    response = HomeView.as_view()(request)
    assert response.status_code == 200
    response.render()
    content = force_text(response.content)
    assert "Mailchimp" in content


@pytest.mark.django_db
def test_form(rf, admin_user, default_shop):
    configuration.cache.clear()

    assert not configuration.get(default_shop, MC_API)
    assert not configuration.get(default_shop, MC_USERNAME)
    assert not configuration.get(default_shop, MC_LIST_ID)
    form = ConfigurationForm(shop=default_shop, data={
        "api_key": MC_API_KEY,
        "list_id": MC_API_LIST_ID,
        "username": MC_API_USERNAME,
    })
    form.full_clean()
    form.save()
    configuration.cache.clear()
    assert configuration.get(default_shop, MC_API) == MC_API_KEY
    assert configuration.get(default_shop, MC_USERNAME) == MC_API_USERNAME
    assert configuration.get(default_shop, MC_LIST_ID) == MC_API_LIST_ID
