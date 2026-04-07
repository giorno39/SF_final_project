document.addEventListener('DOMContentLoaded', function () {
    const describeBtn = document.getElementById('describeWithAiBtn');
    const fileInput = document.getElementById('id_content');
    const descriptionInput = document.getElementById('id_description');
    const statusBox = document.getElementById('aiDescribeStatus');

    if (!describeBtn || !fileInput || !descriptionInput || !statusBox) {
        return;
    }

    function getCsrfToken() {
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        return csrfInput ? csrfInput.value : '';
    }

    function setStatus(message, isError = false) {
        statusBox.textContent = message;
        statusBox.style.color = isError ? '#b00020' : '';
    }

    describeBtn.addEventListener('click', async function () {
        const file = fileInput.files[0];
        const url = describeBtn.dataset.url;

        if (!file) {
            setStatus('Please upload a PDF first.', true);
            return;
        }

        const formData = new FormData();
        formData.append('content', file);

        describeBtn.disabled = true;
        setStatus('Generating description...');

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                },
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Could not generate description.');
            }

            const generatedText = (data.description || '').trim();

            if (!generatedText) {
                throw new Error('The AI returned an empty description.');
            }

            if (descriptionInput.value.trim()) {
                descriptionInput.value += '\n\n' + generatedText;
            } else {
                descriptionInput.value = generatedText;
            }

            setStatus('Description added.');
        } catch (error) {
            setStatus(error.message, true);
        } finally {
            describeBtn.disabled = false;
        }
    });
});