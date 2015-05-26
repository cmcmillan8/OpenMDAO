""" Testing for Problem.check_partial_derivatives."""

from six import iteritems
import unittest

import numpy as np

from openmdao.components.paramcomp import ParamComp
from openmdao.core.group import Group
from openmdao.core.problem import Problem
from openmdao.test.converge_diverge import ConvergeDivergeGroups
from openmdao.test.simplecomps import SimpleArrayComp, SimpleImplicitComp
from openmdao.test.testutil import assert_rel_error


class TestProblemCheckPartials(unittest.TestCase):

    def test_double_diamond_model(self):

        top = Problem()
        top.root = ConvergeDivergeGroups()

        top.setup()
        top.run()

        data = top.check_partial_derivatives()
        #print data

        for key1, val1 in iteritems(data):
            for key2, val2 in iteritems(val1):
                assert_rel_error(self, val2['abs error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][2], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][2], 0.0, 1e-5)

    def test_simple_array_model(self):

        top = Problem()
        top.root = Group()
        top.root.add('comp', SimpleArrayComp())
        top.root.add('p1', ParamComp('x', np.ones([2])))

        top.root.connect('p1:x', 'comp:x')

        top.setup()
        top.run()

        data = top.check_partial_derivatives()

        for key1, val1 in iteritems(data):
            for key2, val2 in iteritems(val1):
                assert_rel_error(self, val2['abs error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][2], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][2], 0.0, 1e-5)

    def test_simple_implicit(self):

        top = Problem()
        top.root = Group()
        top.root.add('comp', SimpleImplicitComp())
        top.root.add('p1', ParamComp('x', 0.5))

        top.root.connect('p1:x', 'comp:x')

        top.setup()
        top.run()

        data = top.check_partial_derivatives()

        for key1, val1 in iteritems(data):
            for key2, val2 in iteritems(val1):
                assert_rel_error(self, val2['abs error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['abs error'][2], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][0], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][1], 0.0, 1e-5)
                assert_rel_error(self, val2['rel error'][2], 0.0, 1e-5)

    def test_bad_size(self):

        class BadComp(SimpleArrayComp):
            def jacobian(self, params, unknowns, resids):
                """Analytical derivatives"""
                J = {}
                J[('y', 'x')] = np.zeros((3, 3))
                return J


        top = Problem()
        top.root = Group()
        top.root.add('comp', BadComp())
        top.root.add('p1', ParamComp('x', np.ones([2])))

        top.root.connect('p1:x', 'comp:x')

        top.setup()
        top.run()

        try:
            data = top.check_partial_derivatives()
        except Exception as err:
            msg = "Jacobian in component 'comp' between the" + \
                " variables 'x' and 'y' is the wrong size. " + \
                "It should be 2 by 2"
            self.assertEquals(str(err), msg)
        else:
            self.fail("Error expected")


if __name__ == "__main__":
    unittest.main()
