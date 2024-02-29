window.addEventListener("load", () => {
    const loader = document.querySelector(".loader");

    if (loader) {
        loader.classList.add("loader--hidden");

        // Remover o loader do HTML depois da página ser carregada.
        loader.addEventListener("transitionend", () => {
            // Verificar se o loader ainda é um filho de document.body
            if (document.body.contains(loader)) {
                document.body.removeChild(loader);
            }
        });
    }
});