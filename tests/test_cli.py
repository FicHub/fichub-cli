from typer.testing import CliRunner
from fichub_cli.cli import app


def test_cli_url(tmpdir):
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(app, [
            '-au https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind'])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_list_url():
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(app, [
            "-al", "https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind,https://www.fanfiction.net/s/13735685/1/we-stand-together"])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_infile():
    runner = CliRunner()

    with runner.isolated_filesystem():

        # create urls.txt with sample urls
        with open('urls.txt', 'w') as f:
            f.write('https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind\nhttps://www.fanfiction.net/s/13735685/1/we-stand-together"')

        result = runner.invoke(app, [
            "-ai", "urls.txt"])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_version():
    runner = CliRunner()

    result = runner.invoke(app, ['--version'])

    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'Version: 0.5.0a'
