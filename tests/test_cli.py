# Copyright 2021 Arbaaz Laskar

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typer.testing import CliRunner
from fichub_cli.cli import app
from fichub_cli import __version__


def test_cli_url(tmpdir):
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app, [
            '-au', 'https://www.fanfiction.net/s/11783284/1/Doppelgängland', '-d'])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_list_url():
    print("----------------------------------------")
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(app, [
            "-al", "https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind,https://www.fanfiction.net/s/13735685/1/we-stand-together", '-d'])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_infile():
    print("----------------------------------------")
    runner = CliRunner()
    with runner.isolated_filesystem():

        # create urls.txt with sample urls
        with open('urls.txt', 'w') as f:
            f.write('https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind\nhttps://www.fanfiction.net/s/13735685/1/we-stand-together"')

        result = runner.invoke(app, [
            "-ai", "urls.txt", '-d'])

    assert not result.exception
    assert result.exit_code == 0


def test_cli_version():
    print("----------------------------------------")
    runner = CliRunner()
    result = runner.invoke(app, ['--version'])

    assert not result.exception
    assert result.exit_code == 0
    assert result.output.strip() == 'fichub-cli: v0.9.4'
