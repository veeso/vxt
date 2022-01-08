from vxt.view.args import CliArgs


def test_cli_args():
    args = CliArgs(["foo", "bar", "omar"], [5, "hi", "0.5"])
    assert 5 == args.get("foo").as_int()
    assert "hi" == args.get("bar").as_str()
    assert 0.5 == args.get("omar").as_float()
