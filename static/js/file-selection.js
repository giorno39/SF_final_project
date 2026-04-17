document.addEventListener("DOMContentLoaded", function () {
  const uploads = document.querySelectorAll(".spec-proof-upload");

  uploads.forEach((upload) => {
    const input = upload.querySelector('input[type="file"]');
    const fileName = upload.querySelector(".spec-proof-file-name");

    if (!input || !fileName) return;

    input.addEventListener("change", function () {
      if (input.files && input.files.length > 0) {
        fileName.textContent = input.files[0].name;
        upload.classList.add("has-file");
      } else {
        fileName.textContent = "No file selected";
        upload.classList.remove("has-file");
      }
    });
  });
});