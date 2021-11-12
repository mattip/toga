import toga
import toga_dummy
from toga.fonts import BOLD, ITALIC, SANS_SERIF, SMALL_CAPS
from toga_dummy.utils import TestCase


class FontTests(TestCase):
    def setUp(self):
        super().setUp()

        self.family = SANS_SERIF
        self.size = 14
        self.style = ITALIC
        self.variant = SMALL_CAPS
        self.weight = BOLD
        self.custom_name = 'my-custom-font'
        self.custom_path = 'resource/custom-font.otf'

        self.font = toga.Font(
            family=self.family,
            size=self.size,
            style=self.style,
            variant=self.variant,
            weight=self.weight)

        # Bind the font to the dummy factory
        self.font.bind(toga_dummy.factory)

        # Register a file-based custom font
        toga.Font.register(self.custom_name, self.custom_path)

    def test_family(self):
        self.assertEqual(self.font.family, self.family)

    def test_size(self):
        self.assertEqual(self.font.size, self.size)

    def test_style(self):
        self.assertEqual(self.font.style, self.style)

    def test_variant(self):
        self.assertEqual(self.font.variant, self.variant)

    def test_weight(self):
        self.assertEqual(self.font.weight, self.weight)

    def test_register(self):
        if self.custom_name not in toga.fonts.REGISTERED_FONTS:
            self.fail("Registered font name not found in toga.fonts.REGISTERED_FONTS")
        if toga.fonts.REGISTERED_FONTS[self.custom_name] != self.custom_path:
            self.fail("Registered font's path is incorrect in toga.fonts.REGISTERED_FONTS")
