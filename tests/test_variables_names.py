from conftest import run_validator_for_test_file


def test_always_ok_for_empty_file():
    errors = run_validator_for_test_file('empty.py', use_strict_mode=True)
    assert not errors


def test_ok_good_names():
    errors = run_validator_for_test_file('ok_names.py', use_strict_mode=True)
    assert not errors


def test_ok_for_short_names_file():
    errors = run_validator_for_test_file('short_names.py', use_strict_mode=True)
    assert len(errors) == 4
    errors = run_validator_for_test_file('short_names.py', use_strict_mode=False)
    assert len(errors) == 3


def test_ok_for_commented_names_file():
    errors = run_validator_for_test_file('commented_names.py', use_strict_mode=True)
    assert not errors


def test_ok_for_blacklisted_names_file():
    errors = run_validator_for_test_file('blacklisted_names.py', use_strict_mode=True)
    assert len(errors) == 2


def test_ok_for_strict_names_file():
    errors = run_validator_for_test_file('strict_names.py', use_strict_mode=False)
    assert not errors
    errors = run_validator_for_test_file('strict_names.py', use_strict_mode=True)
    assert len(errors) == 2


def test_ok_for_builtins_names_file():
    errors = run_validator_for_test_file('builtin_names.py', use_strict_mode=True)
    assert len(errors) == 2


def test_ok_for_class_level_names_file():
    errors = run_validator_for_test_file('class_level_names.py', use_strict_mode=True)
    assert len(errors) == 2
