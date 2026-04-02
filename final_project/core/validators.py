from django.core.exceptions import ValidationError


def file_size_validator(value):
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')


def pdf_only_validator(value):
    name = value.name.lower()
    content_type = getattr(value, 'content_type', None)

    if not name.endswith('.pdf'):
        raise ValidationError('Only PDF files are allowed.')

    if content_type and content_type != 'application/pdf':
        raise ValidationError('Invalid file type. Please upload a PDF.')