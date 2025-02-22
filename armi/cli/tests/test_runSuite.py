# Copyright 2019 TerraPower, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Test for runsuite cli entry point."""
# pylint: disable=missing-function-docstring,missing-class-docstring,protected-access,invalid-name,no-self-use,no-method-argument,import-outside-toplevel
import io
import sys
import unittest

from armi import meta
from armi.cli import ArmiCLI


class TestRunSuiteSuite(unittest.TestCase):
    def test_listCommand(self):
        """Ensure run-suite entry point is registered."""
        acli = ArmiCLI()

        origout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            acli.listCommands()
        finally:
            sys.stdout = origout

        self.assertIn("run-suite", out.getvalue())

    def test_showVersion(self):
        """Test the ArmiCLI.showVersion method."""
        origout = sys.stdout
        try:
            out = io.StringIO()
            sys.stdout = out
            ArmiCLI.showVersion()
        finally:
            sys.stdout = origout

        self.assertIn("armi", out.getvalue())
        self.assertIn(meta.__version__, out.getvalue())


if __name__ == "__main__":
    unittest.main()
