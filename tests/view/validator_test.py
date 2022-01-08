from vxt.view.validator import Validator


def test_validate_optional_positive_number():
    assert Validator.validate_optional_positive_number("5")
    assert Validator.validate_optional_positive_number("")
    assert Validator.validate_optional_positive_number("-2") is not True
    assert Validator.validate_optional_positive_number("aaaa") is not True


def test_validate_negative_optional_number():
    assert Validator.validate_negative_optional_number("-5")
    assert Validator.validate_negative_optional_number("")
    assert Validator.validate_negative_optional_number("2") is not True
    assert Validator.validate_negative_optional_number("aaaa") is not True


def test_validate_positive_number():
    assert Validator.validate_positive_number("5")
    assert Validator.validate_positive_number("") is not True
    assert Validator.validate_positive_number("-2") is not True
    assert Validator.validate_positive_number("aaaa") is not True


def test_validate_number():
    assert Validator.validate_number("5")
    assert Validator.validate_number("-2")
    assert Validator.validate_number("") is not True
    assert Validator.validate_number("aaaa") is not True


def test_validate_track_output_fmt():
    assert Validator.validate_track_output_fmt("%t-%s")


def test_validate_path():
    assert Validator.validate_path("tests")
    assert Validator.validate_path("/tmp/piro/poro/pero") is not True


def test_filter_optional_number():
    assert 5 == Validator.filter_optional_number("5")
    assert Validator.filter_optional_number("") is None


def test_filter_number():
    assert 5 == Validator.filter_number("5")


def test_filter_optional_string():
    assert "hi" == Validator.filter_optional_string("hi")
    assert Validator.filter_optional_string("") is None
