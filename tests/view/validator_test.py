from vxt.view.validator import Validator


def test_validate_optional_positive_number():
    assert Validator.validate_optional_positive_number("5")
    assert Validator.validate_optional_positive_number("")
    assert not Validator.validate_optional_positive_number("-2")
    assert not Validator.validate_optional_positive_number("aaaa")


def test_validate_negative_optional_number():
    assert Validator.validate_negative_optional_number("-5")
    assert Validator.validate_negative_optional_number("")
    assert not Validator.validate_negative_optional_number("2")
    assert not Validator.validate_negative_optional_number("aaaa")


def test_validate_positive_number():
    assert Validator.validate_positive_number("5")
    assert not Validator.validate_positive_number("")
    assert not Validator.validate_positive_number("-2")
    assert not Validator.validate_positive_number("aaaa")


def test_validate_number():
    assert Validator.validate_number("5")
    assert Validator.validate_number("-2")
    assert not Validator.validate_number("")
    assert not Validator.validate_number("aaaa")


def test_validate_track_output_fmt():
    assert Validator.validate_track_output_fmt("%t-%s")


def test_validate_path():
    assert Validator.validate_path("tests")
    assert not Validator.validate_path("/tmp/piro/poro/pero")


def test_filter_optional_number():
    assert 5 == Validator.filter_optional_number("5")
    assert Validator.filter_optional_number("") is None


def test_filter_number():
    assert 5 == Validator.filter_number("5")


def test_filter_optional_string():
    assert "hi" == Validator.filter_optional_string("hi")
    assert Validator.filter_optional_string("") is None
