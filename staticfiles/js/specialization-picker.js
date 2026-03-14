document.addEventListener("DOMContentLoaded", function () {
    const picker = document.getElementById("specPicker");
    const searchInput = document.getElementById("specSearch");
    const dropdown = document.getElementById("specDropdown");
    const selectedBox = document.getElementById("specSelected");
    const options = Array.from(document.querySelectorAll(".spec-option"));
    const checkboxes = Array.from(document.querySelectorAll(".spec-hidden-checkbox input[type='checkbox']"));

    function getCheckboxByValue(value) {
        return checkboxes.find(cb => cb.value === value);
    }

    function renderSelected() {
        selectedBox.innerHTML = "";

        checkboxes.forEach(cb => {
            if (cb.checked) {
                const option = options.find(opt => opt.dataset.value === cb.value);
                if (!option) return;

                const tag = document.createElement("span");
                tag.className = "spec-tag";
                tag.textContent = option.dataset.text;

                const removeBtn = document.createElement("button");
                removeBtn.type = "button";
                removeBtn.className = "spec-tag-remove";
                removeBtn.innerHTML = "&times;";
                removeBtn.addEventListener("click", function () {
                    cb.checked = false;
                    renderSelected();
                    filterOptions();
                });

                tag.appendChild(removeBtn);
                selectedBox.appendChild(tag);
            }
        });

        options.forEach(option => {
            const cb = getCheckboxByValue(option.dataset.value);
            option.style.display = cb && cb.checked ? "none" : "block";
        });
    }

    function filterOptions() {
        const query = searchInput.value.trim().toLowerCase();

        options.forEach(option => {
            const cb = getCheckboxByValue(option.dataset.value);
            if (cb && cb.checked) {
                option.style.display = "none";
                return;
            }

            option.style.display = option.dataset.label.includes(query) ? "block" : "none";
        });
    }

    searchInput.addEventListener("focus", function () {
        dropdown.classList.add("show");
        filterOptions();
    });

    searchInput.addEventListener("input", function () {
        dropdown.classList.add("show");
        filterOptions();
    });

    options.forEach(option => {
        option.addEventListener("click", function () {
            const cb = getCheckboxByValue(option.dataset.value);
            if (cb) {
                cb.checked = true;
                searchInput.value = "";
                renderSelected();
                filterOptions();
                searchInput.focus();
            }
        });
    });

    document.addEventListener("click", function (event) {
        if (!picker.contains(event.target)) {
            dropdown.classList.remove("show");
        }
    });

    renderSelected();
});