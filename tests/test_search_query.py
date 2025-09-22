from ymir.core.models.search_query import SearchQuery


def test_search_query_string_representation():
    """Test the string representation of SearchQuery."""
    query = SearchQuery(service="gmail", username="admin")
    assert "gmail" in str(query)
    assert "admin" in str(query)

    empty_query = SearchQuery()
    assert "show all entries" in str(empty_query)


def test_search_query_convenience_methods():
    """Test the convenience factory methods."""
    text_query = SearchQuery.create_text_search("google")
    assert text_query.search_text == "google"

    service_query = SearchQuery.create_service_search("github")
    assert service_query.service == "github"

    tag_query = SearchQuery.create_tag_search(["work", "urgent"])
    assert tag_query.tags == ["work", "urgent"]
