// Mecânica que esconde o loader após o carregamento da página
window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");

    loader.classList.add("loader--hidden");

    // Remover o loader do HTML depois da página ser carregada.
    loader.addEventListener("transitionend", () => {
        document.body.removeChild(loader);
    });
});