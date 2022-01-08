from vxt.view.validator import Validator


def test_validate_optional_positive_number():
    assert True == Validator.validate_optional_positive_number("5")
    assert True == Validator.validate_optional_positive_number("")
    assert True != Validator.validate_optional_positive_number("-2")
    assert True != Validator.validate_optional_positive_number("aaaa")


def test_validate_negative_optional_number():
    assert True == Validator.validate_negative_optional_number("-5")
    assert True == Validator.validate_negative_optional_number("")
    assert True != Validator.validate_negative_optional_number("2")
    assert True != Validator.validate_negative_optional_number("aaaa")


def test_validate_positive_number():
    assert True == Validator.validate_positive_number("5")
    assert True != Validator.validate_positive_number("")
    assert True != Validator.validate_positive_number("-2")
    assert True != Validator.validate_positive_number("aaaa")


def test_validate_number():
    assert True == Validator.validate_number("5")
    assert True == Validator.validate_number("-2")
    assert True != Validator.validate_number("")
    assert True != Validator.validate_number("aaaa")


def test_validate_track_output_fmt():
    assert True == Validator.validate_track_output_fmt("%t-%s")


def test_validate_path():
    assert True == Validator.validate_path("tests")
    assert True != Validator.validate_path("/tmp/piro/poro/pero")


def test_filter_optional_number():
    assert 5 == Validator.filter_optional_number("5")
    assert None == Validator.filter_optional_number("")


def test_filter_number():
    assert 5 == Validator.filter_number("5")


def test_filter_optional_string():
    assert "hi" == Validator.filter_optional_string("hi")
    assert None == Validator.filter_optional_string("")
