document.addEventListener("DOMContentLoaded", function () {
    const disabledLinks = document.querySelectorAll("[data-demo-disabled='true']");

    disabledLinks.forEach(function (link) {
        link.addEventListener("click", function (event) {
            event.preventDefault();
            alert("Bu GitHub Pages static demo. Backend funksiyalar demo rejimida ishlamaydi.");
        });
    });

    const forms = document.querySelectorAll("form");

    forms.forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            alert("Bu GitHub Pages static demo. Formalar backend server talab qiladi.");
        });
    });
});