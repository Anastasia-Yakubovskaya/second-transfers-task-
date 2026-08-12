import unittest
from adaptive_map import AdaptiveMap


class TestAdaptiveMap(unittest.TestCase):

    def test_empty_map(self):
        m = AdaptiveMap()

        self.assertEqual(m.size, 0)
        self.assertIsNone(m.storage)
        self.assertFalse(m.contains_key("key"))

        with self.assertRaises(KeyError):
            m.get("key")

    def test_one_element(self):
        m = AdaptiveMap()

        m.put("a", 100)
        self.assertEqual(m.size, 1)
        self.assertTrue(m.contains_key("a"))
        self.assertEqual(m.get("a"), 100)

        # Перезапись ключа
        m.put("a", 200)
        self.assertEqual(m.size, 1)
        self.assertEqual(m.get("a"), 200)

    def test_array_storage(self):
        m = AdaptiveMap()

        m.put(1, "one")
        m.put(2, "two")

        self.assertEqual(m.size, 2)
        self.assertTrue(isinstance(m.storage, list))
        self.assertEqual(len(m.storage), 5)

        m.put(3, "three")
        m.put(4, "four")
        m.put(5, "five")

        self.assertEqual(m.size, 5)
        self.assertEqual(m.get(3), "three")
        self.assertEqual(m.get(5), "five")

        m.put(3, "NEW_THREE")
        self.assertEqual(m.get(3), "NEW_THREE")
        self.assertEqual(m.size, 5)

    def test_dict_migration(self):
        m = AdaptiveMap()

        for i in range(1, 6):
            m.put(f"k{i}", i)

        self.assertTrue(isinstance(m.storage, list))

        # 6-й элемент триггерит переход на dict
        m.put("k6", 6)

        self.assertEqual(m.size, 6)
        self.assertTrue(isinstance(m.storage, dict))

        for i in range(1, 7):
            self.assertTrue(m.contains_key(f"k{i}"))
            self.assertEqual(m.get(f"k{i}"), i)

    def test_different_key_types(self):
        m = AdaptiveMap()

        m.put(100, "number")
        m.put("text_key", "string")
        m.put((1, 2), "tuple")

        self.assertEqual(m.get(100), "number")
        self.assertEqual(m.get("text_key"), "string")
        self.assertEqual(m.get((1, 2)), "tuple")

    def test_missing_key_exception(self):
        m = AdaptiveMap()

        m.put("x", 10)
        m.put("y", 20)

        with self.assertRaises(KeyError):
            m.get("z")


if __name__ == "__main__":
    unittest.main()