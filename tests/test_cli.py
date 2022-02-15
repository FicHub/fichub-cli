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

from fichub_cli.cli import main
import os


def test_cli_url(tmp_path):
    tmp_dir = tmp_path

    try:
        main(["-au", "https://www.fanfiction.net/s/12933896/1/Things-you-cannot-leave-behind",
              "-o", f"{tmp_dir}"])
    except Exception as e:
        print(e)


def test_cli_list_url(tmp_path):
    tmp_dir = tmp_path

    try:
        main(["-al", "https://www.fanfiction.net/s/5199602,https://www.fanfiction.net/s/6353112/1/Man-Made-Gods",
             "-o", f"{tmp_dir}"])
    except Exception as e:
        print(e)


def test_cli_infile(tmp_path):
    tmp_dir = tmp_path

    url_file = str(os.path.join(tmp_dir, 'urls.txt'))
    # create urls.txt with sample urls
    with open(url_file, 'w') as f:
        f.write('https://www.fanfiction.net/s/11730208/1/Darth-Vader-Hero-of-Naboo\nhttps://www.fanfiction.net/s/13735685/1/we-stand-together\nhttps://m.fanfiction.net/s/5599903/1/')

    try:
        main(["-ai", url_file, "-o", f"{tmp_dir}"])
    except Exception as e:
        print(e)


def test_cli_version(capsys):
    try:
        main(["--version"])
    except SystemExit:
        pass
    output = capsys.readouterr().out
    assert output.strip() == 'fichub-cli: v0.5.3'
