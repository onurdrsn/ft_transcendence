function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showPass(inputPassword) {
    const pass = document.getElementById(inputPassword)
    const icon = document.querySelector('.eye-icon')
    if (pass && icon) {
        if (pass.type === "password") {
            icon.innerHTML = '🙈'
            pass.type = "text"
        } else if (pass.type === "text") {
            pass.type = "password"
            icon.innerHTML = '👁️'
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    let languageSelect = document.querySelector('#languageForm select[name="language"]');
    languageSelect.addEventListener("change", function() {
        document.getElementById('languageForm').submit();
    });
});
