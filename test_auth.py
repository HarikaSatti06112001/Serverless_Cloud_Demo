# test_auth.py

import unittest
from auth import authenticate_user, can_invoke_runtime

class TestAuthentication(unittest.TestCase):
    def test_authenticate_user_valid(self):
        self.assertTrue(authenticate_user("user1"))

    def test_authenticate_user_invalid(self):
        self.assertFalse(authenticate_user("nonexistent_user"))

class TestAuthorization(unittest.TestCase):
    def test_can_invoke_runtime_alpha(self):
        self.assertTrue(can_invoke_runtime("user1", "RuntimeAlpha"))

    def test_can_invoke_runtime_alpha_unauthorized(self):
        self.assertFalse(can_invoke_runtime("user2", "RuntimeAlpha"))

    def test_can_invoke_runtime_beta(self):
        self.assertTrue(can_invoke_runtime("user2", "RuntimeBeta"))

    def test_can_invoke_runtime_unknown(self):
        self.assertFalse(can_invoke_runtime("user1", "UnknownRuntime"))

if __name__ == '__main__':
    unittest.main()
