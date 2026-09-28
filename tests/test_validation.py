from layout_optimizer.models import Area, Factory
from layout_optimizer.validation import validate_area, validate_factory


def test_valid_factory_has_no_errors():
    factory = Factory(50, 50)

    assert validate_factory(factory) == []


def test_invalid_factory_width_returns_error():
    factory = Factory(-10, 50)

    errors = validate_factory(factory)

    assert "工場の横幅は0より大きい値を入力してください。" in errors


def test_valid_area_has_no_errors():
    area = Area("cutting_machine", "切断機", 2, 4, 3)

    assert validate_area(area) == []


def test_invalid_area_returns_errors():
    area = Area("", "", 0, -4, 0)

    errors = validate_area(area)

    assert "設備IDを入力してください。" in errors
    assert "設備名を入力してください。" in errors
    assert "設備数は1以上を入力してください。" in errors
    assert "設備の幅は0より大きい値を入力してください。" in errors
    assert "設備の奥行きは0より大きい値を入力してください。" in errors