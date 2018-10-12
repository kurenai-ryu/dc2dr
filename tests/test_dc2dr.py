#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_dc2dr
----------------------------------

Tests for `dc2dr` module.
"""

import pytest

from contextlib import contextmanager
from click.testing import CliRunner

import yaml
from dc2dr import cli
from dc2dr import parser

FILE_PATH = 'tests/docker-compose.yml'

class TestDc2dr(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_order_is_correct(self):
        run_commands = parser.run_commands(FILE_PATH)

        assert '--name=db' in run_commands[0]
        assert '--name=api2' in run_commands[1]
        assert '--name=api1' in run_commands[2]
        assert '--name=web' in run_commands[3]

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, [FILE_PATH])
        assert result.exit_code == 0
        assert 'docker run' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output

    def test_no_links(self):
        runner = CliRunner()
        result = runner.invoke(cli.main, ['tests/no-links.yml'])
        assert result.exit_code == 0
        commands = [
                'docker run -d --name=nats  -p 4222:4222  --expose=4222 nats:0.8.1',
                'docker run -d --name=ldapserver  -p 9389:389 openldap --loglevel debug',
                'docker run -d --name=mysql  -p 3306:3306  --expose=3306',
                '-e MYSQL_PASSWORD="super-secret"',
                '-e MYSQL_USER="user"',
                'advancedtelematic/mariadb:stable --character-set-server=utf8 --collation-server=utf8_unicode_ci --max-connections=1000']
        for s in commands:
            assert s in result.output

    @classmethod
    def teardown_class(cls):
        pass
