const serviceItems = document.querySelectorAll('.service');

serviceItems.forEach(item => {
    const title = item.querySelector('.service-title');
    const details = item.querySelector('.service-details');

    title.addEventListener('click', () => {
        // Fecha todos os outros serviços antes de abrir o atual
        serviceItems.forEach(service => {
            if (service !== item) {
                service.classList.remove('show');
            }
        });

        // Alterna a classe do item clicado
        item.classList.toggle('show');
    });
});
