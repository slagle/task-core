"""unit tests of the inventory module"""
import unittest
from unittest import mock
from task_core import inventory
from task_core import exceptions as ex

DUMMY_INVENTORY_DATA = """
hosts:
  host-a:
    role: keystone
  host-b:
    role: basic
"""

DUMMY_ROLES_DATA = """
basic:
  services:
    - chronyd
    - repos
keystone:
  services:
    - chronyd
    - repos
    - mariadb
    - openstack-keystone
"""


class TestInventory(unittest.TestCase):
    """Test Inventory object"""

    def test_file_data(self):
        """test inventory file"""
        hosts = {"host-a": {"role": "keystone"}, "host-b": {"role": "basic"}}

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=DUMMY_INVENTORY_DATA)
        ) as open_mock:
            obj = inventory.Inventory("/foo/bar")
            open_mock.assert_called_with("/foo/bar")
            self.assertEqual(obj.data, {"hosts": hosts})
            self.assertEqual(obj.hosts, hosts)
            self.assertEqual(obj.get_role_hosts(), hosts.keys())

    def test_role_filter(self):
        """test getting hosts by role"""

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=DUMMY_INVENTORY_DATA)
        ) as open_mock:
            obj = inventory.Inventory("/foo/bar")
            open_mock.assert_called_with("/foo/bar")
            self.assertEqual(obj.get_role_hosts("keystone"), ["host-a"])


class TestRoles(unittest.TestCase):
    """Test Roles object"""

    def test_file_data(self):
        """test roles file"""

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=DUMMY_ROLES_DATA)
        ) as open_mock:
            obj = inventory.Roles("/foo/bar")
            open_mock.assert_called_with("/foo/bar")
            # todo: data
            self.assertEqual(obj.roles, {"basic": mock.ANY, "keystone": mock.ANY})
            self.assertTrue(isinstance(obj.roles.get("basic"), inventory.Role))
            self.assertTrue(isinstance(obj.roles.get("keystone"), inventory.Role))
            self.assertEqual(obj.get_services("basic"), ["chronyd", "repos"])

    def test_missing_role(self):
        """test roles file"""

        with mock.patch(
            "builtins.open", mock.mock_open(read_data=DUMMY_ROLES_DATA)
        ) as open_mock:
            obj = inventory.Roles("/foo/bar")
            open_mock.assert_called_with("/foo/bar")
            self.assertRaises(ex.InvalidRole, obj.get_services, "doesnotexist")


class TestRole(unittest.TestCase):
    """Test Role object"""

    def test_role(self):
        """test role object"""
        obj = inventory.Role("foo", ["bar"])
        self.assertEqual(obj.name, "foo")
        self.assertEqual(obj.services, ["bar"])