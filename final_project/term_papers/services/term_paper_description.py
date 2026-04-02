import openai
from django.conf import settings

from final_project.ai.client import get_openai_client


def _validate_uploaded_pdf(uploaded_file):
    if not uploaded_file:
        raise ValueError('Please upload a PDF first.')

    file_name = (uploaded_file.name or '').lower()
    content_type = getattr(uploaded_file, 'content_type', None)

    if not file_name.endswith('.pdf'):
        raise ValueError('Only PDF files are allowed.')

    if content_type and content_type != 'application/pdf':
        raise ValueError('Invalid file type. Please upload a PDF.')


def describe_term_paper_with_ai(uploaded_file):
    _validate_uploaded_pdf(uploaded_file)

    client = get_openai_client()

    uploaded_file.seek(0)

    uploaded = client.files.create(
        file=(
            uploaded_file.name,
            uploaded_file.file,
            uploaded_file.content_type or 'application/pdf',
        ),
        purpose='user_data',
    )

    response = client.responses.create(
        model=settings.OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You read university term paper PDFs and produce a short, clear "
                    "description for a form field. Return plain text only."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Read this PDF and write a concise description of the term paper. "
                            "Include the topic, requirements, expected deliverables, and any "
                            "important constraints."
                        ),
                    },
                    {
                        "type": "input_file",
                        "file_id": uploaded.id,
                    },
                ],
            },
        ],
    )

    description = (response.output_text or '').strip()

    if not description:
        raise ValueError('The AI returned an empty description.')

    return description