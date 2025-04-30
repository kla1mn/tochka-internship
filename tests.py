import unittest
from run import check_capacity


class Tests(unittest.TestCase):
    def test_true1(self):
        max_capacity = 2
        guests = [
            {"name": "3", "check-in": "2021-01-15", "check-out": "2021-01-21"},
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-20"},
        ]
        self.assertTrue(check_capacity(max_capacity, guests))

    def test_false1(self):
        max_capacity = 2
        guests = [
            {"name": "3", "check-in": "2021-01-15", "check-out": "2021-01-21"},
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-16"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-20"},

        ]
        self.assertFalse(check_capacity(max_capacity, guests))

    def test_single_guest(self):
        max_capacity = 1
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"}
        ]
        self.assertTrue(check_capacity(max_capacity, guests))

    def test_multiple_guests_with_same_check_out(self):
        max_capacity = 2
        guests = [
            {"name": "3", "check-in": "2021-01-13", "check-out": "2021-01-15"},
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-15"},

        ]
        self.assertFalse(check_capacity(max_capacity, guests))

    def test_multiple_guests_with_exactly_same_check_in_and_check_out(self):
        max_capacity = 3
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-12"},
            {"name": "3", "check-in": "2021-01-10", "check-out": "2021-01-12"},
            {"name": "2", "check-in": "2021-01-10", "check-out": "2021-01-12"},

        ]
        self.assertTrue(check_capacity(max_capacity, guests))

    def test_no_guest_overlap(self):
        max_capacity = 3
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-12"},
            {"name": "2", "check-in": "2021-01-13", "check-out": "2021-01-15"},
            {"name": "3", "check-in": "2021-01-16", "check-out": "2021-01-18"},
        ]
        self.assertTrue(check_capacity(max_capacity, guests))

    def test_edge_case_no_guests(self):
        max_capacity = 2
        guests = []
        self.assertTrue(check_capacity(max_capacity, guests))

    def test_edge_case_zero_capacity(self):
        max_capacity = 0
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-12"}
        ]
        self.assertFalse(check_capacity(max_capacity, guests))

    def test_edge_case_one_capacity_overlapping_guests(self):
        max_capacity = 1
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-20"},
        ]
        self.assertFalse(check_capacity(max_capacity, guests))

    def test_multiple_guests_with_overlapping_stays(self):
        max_capacity = 2
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-15"},
            {"name": "2", "check-in": "2021-01-12", "check-out": "2021-01-18"},
            {"name": "3", "check-in": "2021-01-14", "check-out": "2021-01-20"},
        ]
        self.assertFalse(check_capacity(max_capacity, guests))

    def test_max_capacity_reached(self):
        max_capacity = 3
        guests = [
            {"name": "1", "check-in": "2021-01-10", "check-out": "2021-01-12"},
            {"name": "2", "check-in": "2021-01-11", "check-out": "2021-01-14"},
            {"name": "3", "check-in": "2021-01-12", "check-out": "2021-01-16"},
            {"name": "4", "check-in": "2021-01-13", "check-out": "2021-01-15"},
        ]
        self.assertTrue(check_capacity(max_capacity, guests))
