import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestListbyTag:
    def test_tag_url(self, client, post_factory):
        post_factory(title="test-post", tags=["test-tag"])
        url = reverse("post_by_tag", kwargs={"tag": "test-tag"})
        response = client.get(url)
        assert response.status_code == 200

    def test_tag_htmx_fragment(self, client, post_factory):
        post_factory(title="test-post", tags=["test-tag"])
        headers = {"HTTP_HX-Request": "true"}
        url = reverse("post_by_tag", kwargs={"tag": "test-tag"})
        response = client.get(url, **headers)
        assertTemplateUsed(response, "how/components/post-list-elements-tags.html")

    def test_tag_filter(self, client, post_factory):
        x = post_factory(title="test-post", tags=["test-tag"])
        url = reverse("post_by_tag", kwargs={"tag": "test-tag"})
        response = client.get(url)
        assert x.tags.all()[0].name == response.context["tag"]
