from benchmark.pydantic_validator import validate_against_schema


def test_generic_schema_validation():
    out = validate_against_schema({"status": "success", "message": "ok"})
    assert out["valid"] is True


def test_invalid_schema():
    out = validate_against_schema({"foo": "bar"})
    assert out["valid"] is False


