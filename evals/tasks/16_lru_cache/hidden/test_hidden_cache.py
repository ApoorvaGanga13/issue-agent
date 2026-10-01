from cache import LRUCache


def test_update_existing_refreshes():
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    c.put("a", 10)
    c.put("c", 3)
    assert c.get("a") == 10
    assert c.get("b") == -1


def test_capacity_one():
    c = LRUCache(1)
    c.put("a", 1)
    c.put("b", 2)
    assert c.get("a") == -1
    assert c.get("b") == 2


def test_missing_key():
    assert LRUCache(2).get("zzz") == -1
