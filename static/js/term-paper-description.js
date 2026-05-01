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
            setStatus('Моля, качете PDF файл първо.', true);
            return;
        }

        const formData = new FormData();
        formData.append('content', file);

        describeBtn.disabled = true;
        setStatus('Генериране на описание...');

        try {
            const response = await fetch(url, {
                method: 'POST',
                body: formData,
                credentials: 'same-origin',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            });

            const contentType = response.headers.get('content-type') || '';

            if (!contentType.includes('application/json')) {
                const html = await response.text();
                console.error('Expected JSON, got HTML/text response:', html);
                throw new Error('Сървърът върна неочакван отговор. Проверете конзолата за подробности.');
            }

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Описанието не можа да бъде генерирано.');
            }

            const generatedText = (data.description || '').trim();

            if (!generatedText) {
                throw new Error('AI върна празно описание.');
            }

            if (descriptionInput.value.trim()) {
                descriptionInput.value += '\n\n' + generatedText;
            } else {
                descriptionInput.value = generatedText;
            }

            setStatus('Описанието е добавено.');
        } catch (error) {
            setStatus(error.message, true);
        } finally {
            describeBtn.disabled = false;
        }
    });
});