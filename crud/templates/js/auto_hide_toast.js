setTimeout(() => {
    const toast = document.getElementById('toast-message');

    if (toast) {
        toast.style.transition = "0.5s";
        toast.style.opacity = "0";

        setTimeout(() => {
            toast.remove();
        }, 500);
    }
}, 3000);