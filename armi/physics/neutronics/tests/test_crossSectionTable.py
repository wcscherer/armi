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
"""Tests for cross section table for depletion."""
# pylint: disable=missing-function-docstring,missing-class-docstring,protected-access,invalid-name,no-self-use,no-method-argument,import-outside-toplevel
import unittest

from armi.nuclearDataIO.cccc import isotxs
from armi.physics.neutronics.isotopicDepletion import (
    crossSectionTable,
    isotopicDepletionInterface as idi,
)
from armi.physics.neutronics.latticePhysics import ORDER
from armi.reactor.flags import Flags
from armi.reactor.tests.test_blocks import loadTestBlock
from armi.reactor.tests.test_reactors import loadTestReactor
from armi.settings import Settings
from armi.tests import ISOAA_PATH


class TestCrossSectionTable(unittest.TestCase):
    def test_makeTable(self):
        obj = loadTestBlock()
        obj.p.mgFlux = range(33)
        core = obj.getAncestorWithFlags(Flags.CORE)
        core.lib = isotxs.readBinary(ISOAA_PATH)
        table = crossSectionTable.makeReactionRateTable(obj)

        self.assertEqual(len(obj.getNuclides()), len(table))
        self.assertEqual(obj.getName(), "B0001-000")

        self.assertEqual(table.getName(), "B0001-000")
        self.assertTrue(table.hasValues())

        xSecTable = table.getXsecTable()
        self.assertEqual(len(xSecTable), 11)
        self.assertIn("xsecs", xSecTable[0])
        self.assertIn("mcnpId", xSecTable[-1])

    def test_isotopicDepletionInterface(self):
        _o, r = loadTestReactor()
        cs = Settings()

        aid = idi.AbstractIsotopicDepleter(r, cs)
        self.assertIsNone(aid.efpdToBurn)
        self.assertEqual(len(aid._depleteByName), 0)

        self.assertEqual(len(aid.getToDeplete()), 0)
        self.assertEqual(ORDER, 5.0)


if __name__ == "__main__":
    unittest.main()
