import unittest
import tempfile
import os
from Chatbot.cache import llm_cache
from Chatbot.cache.llm_cache import ColorLLMCache


class TestColorLLMCache(unittest.TestCase):

    def setUp(self):
        self.cache = ColorLLMCache.get_instance()
        self.cache.clear()

    def test_rgb_set_and_get(self):
        self.cache.store_rgb("peachy beige", (243, 207, 183))
        self.assertEqual((243, 207, 183), self.cache.get_rgb("peachy beige"))

    def test_simplified_set_and_get(self):
        self.cache.store_simplified("peachy", ["light peach"])
        self.assertEqual(["light peach"], self.cache.get_simplified("peachy"))

    def test_tuple_conversion_from_list(self):
        self.cache._rgb_cache["sunset orange"] = [250, 100, 80]
        self.assertEqual((250, 100, 80), self.cache.get_rgb("sunset orange"))

    def test_clear_cache(self):
        self.cache.store_rgb("warm pink", (200, 120, 140))
        self.cache.store_simplified("dusty", ["muted rose"])
        self.cache.clear()
        self.assertIsNone(self.cache.get_rgb("warm pink"))
        self.assertEqual([], self.cache.get_simplified("dusty"))

    def test_save_and_load_file(self):
        self.cache.store_rgb("cool mint", (180, 255, 240))
        self.cache.store_simplified("minty", ["cool mint"])
        with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
            path = tmpfile.name
        self.cache._path = path
        self.cache.save()

        new_cache = ColorLLMCache.get_instance()
        new_cache.clear()
        new_cache._path = path
        new_cache.load()

        self.assertEqual((180, 255, 240), new_cache.get_rgb("cool mint"))
        self.assertEqual(["cool mint"], new_cache.get_simplified("minty"))
        os.remove(path)

    def test_singleton_identity(self):
        self.assertIs(ColorLLMCache.get_instance(), ColorLLMCache.get_instance())

    def test_case_insensitive_keys(self):
        self.cache.store_rgb("Rose Gold", (255, 200, 180))
        self.assertEqual((255, 200, 180), self.cache.get_rgb("rose gold"))

    def test_strip_keys_on_get(self):
        self.cache.store_rgb("   rosy pink ", (230, 150, 160))
        self.assertEqual((230, 150, 160), self.cache.get_rgb("rosy pink"))

    def test_store_rgb_saves_as_list(self):
        self.cache.store_rgb("test color", (1, 2, 3))
        self.assertIsInstance(self.cache._rgb_cache["test color"], list)

    def test_store_and_get_multiple_simplified(self):
        self.cache.store_simplified("sunrise", ["orange pink", "warm coral"])
        self.assertEqual(["orange pink", "warm coral"], self.cache.get_simplified("sunrise"))
