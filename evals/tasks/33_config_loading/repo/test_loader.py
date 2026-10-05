from loader import load


def test_port_is_a_number():
    assert load({"APP_PORT": "9000"})["port"] == 9000


def test_name_stays_text():
    assert load({"APP_NAME": "shop"})["name"] == "shop"
