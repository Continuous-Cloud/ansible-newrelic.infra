# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.plugins.lookup import LookupBase
import logging
import subprocess
import json
import random
import string


DOCUMENTATION = """
lookup: obfuscate_string
author: Mike Morency
version_added: "1"
short_description: use new relic to obfuscate a string
description:
    - This lookup returns an obfuscated version of a string using the new relic cli
options:
    seed:
        description:
        - The seed used to create the obfuscation key. Setting this is suggested so the same value is
            used on re-runs.
        required: True
        type: str
"""

USAGE = """
    - name: No Seed Example
      debug:
        msg: "{{ lookup('obfuscate_string', 'test_string') }}"

    - name: Set The Seed To Get Consistent Output On Re-Runs
      debug:
        msg: "{{ lookup('obfuscate_string', 'test_string', seed=inventory_hostname) }}"
"""


def check_newrelic_command():
    """
    Checks that the newrelic cli tool is installed and on the path
    """
    logging.info("Checking the thycotic api health before continuing")
    try:
        cmd_run = subprocess.run(
            ["newrelic", "--version"],
            shell=True, check=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if cmd_run.stderr:
            raise Exception(cmd_run.stderr)
    except Exception as e:
        logging.fatal(e)
        raise Exception(
            "Unable to find the newrelic cli command. "
            "Is it installed and on the path? You can install it with the nr_cli role"
        )
    logging.info(cmd_run.stdout)


def obfuscate_value(input_value, obfuscation_key):
    """
    Uses the cli tool to obfuscate a string value
    """
    logging.info("Obfuscating value")
    try:
        cmd_run = subprocess.run(
            f"newrelic agent config obfuscate --value '{input_value}' --key '{obfuscation_key}'",
            shell=True, check=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        if cmd_run.stderr:
            raise Exception(cmd_run.stderr)
    except Exception as e:
        logging.fatal(e)
        raise

    return json.loads(cmd_run.stdout.decode("utf-8"))['obfuscatedValue']


def generate_obfuscation_key(seed=None):
    if seed:
        random.seed(seed)

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        # lookups in general are expected to both take a list as input and output a list
        # this is done so they work with the looping construct 'with_'.
        ret = []

        obfuscation_key = generate_obfuscation_key(kwargs.get('seed', None))
        check_newrelic_command()

        for input_value in terms:
            ret += [{
                "secret": obfuscate_value(input_value, obfuscation_key),
                "key": obfuscation_key
            }]

        return ret
