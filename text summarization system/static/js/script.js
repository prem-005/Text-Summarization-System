document.addEventListener("DOMContentLoaded", () => {
  const file = document.querySelector('input[type="file"]');
  const textarea = document.querySelector("textarea");
  if (file) {
    file.addEventListener("change", () => {
      if (file.files.length) textarea.placeholder = "Selected: " + file.files[0].name;
    });
  }
});
