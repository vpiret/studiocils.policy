# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from studiocils.policy.testing import STUDIOCILS_POLICY_INTEGRATION_TESTING

import unittest


class TestSetup(unittest.TestCase):
    """Test that studiocils.policy is properly installed."""

    layer = STUDIOCILS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if studiocils.policy is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'studiocils.policy'))

    def test_browserlayer(self):
        """Test that IStudiocilsPolicyLayer is registered."""
        from studiocils.policy.interfaces import (
            IStudiocilsPolicyLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IStudiocilsPolicyLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = STUDIOCILS_POLICY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['studiocils.policy'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if studiocils.policy is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'studiocils.policy'))

    def test_browserlayer_removed(self):
        """Test that IStudiocilsPolicyLayer is removed."""
        from studiocils.policy.interfaces import \
            IStudiocilsPolicyLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IStudiocilsPolicyLayer,
            utils.registered_layers())
