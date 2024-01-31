// Seu JavaScript (script.js)

document.addEventListener("DOMContentLoaded", function () {
    // Exibe as mensagens flash
    function showFlashMessages() {
        var flashMessages = document.querySelectorAll(".flash-message");

        flashMessages.forEach(function (message, index) {
            setTimeout(function () {
                message.style.opacity = "1";
            }, index * 500); // Adicionando um atraso entre cada mensagem (ajuste conforme necessário)
        });
    }

    // Esconde as mensagens flash após um intervalo de tempo (exemplo: 3 segundos)
    function hideFlashMessages() {
        var flashMessages = document.querySelectorAll(".flash-message");

        flashMessages.forEach(function (message) {
            setTimeout(function () {
                message.style.opacity = "0";
            }, 3000); // 3000 milissegundos = 3 segundos (ajuste conforme necessário)
        });
    }

    // Exibe as mensagens flash quando a página carrega
    showFlashMessages();

    // Esconde as mensagens flash após um intervalo de tempo
    hideFlashMessages();
});
