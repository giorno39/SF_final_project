from types import SimpleNamespace

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from final_project.core.validators import file_size_validator, pdf_only_validator


class FileSizeValidatorTests(SimpleTestCase):
    LIMIT = 2 * 1024 * 1024

    def test_file_size__when_below_limit__expect_no_error(self):
        small_file = SimpleNamespace(size=self.LIMIT - 1, name='ok.pdf')

        # Should not raise.
        self.assertIsNone(file_size_validator(small_file))

    def test_file_size__when_exactly_on_limit__expect_no_error(self):
        on_limit_file = SimpleNamespace(size=self.LIMIT, name='ok.pdf')

        self.assertIsNone(file_size_validator(on_limit_file))

    def test_file_size__when_above_limit__expect_validation_error(self):
        big_file = SimpleNamespace(size=self.LIMIT + 1, name='big.pdf')

        with self.assertRaises(ValidationError):
            file_size_validator(big_file)


class PdfOnlyValidatorTests(SimpleTestCase):
    def test_pdf_only__when_pdf_name_and_pdf_content_type__expect_no_error(self):
        valid = SimpleNamespace(name='paper.pdf', content_type='application/pdf')

        self.assertIsNone(pdf_only_validator(valid))

    def test_pdf_only__when_name_is_uppercase_pdf__expect_no_error(self):
        valid = SimpleNamespace(name='PAPER.PDF', content_type='application/pdf')

        self.assertIsNone(pdf_only_validator(valid))

    def test_pdf_only__when_no_content_type_attribute__expect_no_error(self):
        # content_type is optional; only the extension is mandatory.
        valid = SimpleNamespace(name='paper.pdf')

        self.assertIsNone(pdf_only_validator(valid))

    def test_pdf_only__when_not_pdf_extension__expect_validation_error(self):
        invalid = SimpleNamespace(name='paper.txt', content_type='text/plain')

        with self.assertRaises(ValidationError):
            pdf_only_validator(invalid)

    def test_pdf_only__when_pdf_extension_but_wrong_content_type__expect_validation_error(self):
        invalid = SimpleNamespace(name='paper.pdf', content_type='text/plain')

        with self.assertRaises(ValidationError):
            pdf_only_validator(invalid)
