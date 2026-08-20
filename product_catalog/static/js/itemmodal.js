
function openModal(card) {

    document.getElementById("modalTitle").innerText =
        card.dataset.title;

    document.getElementById("modalDescription").innerText =
        card.dataset.description;

    document.getElementById("modalImage").src =
        card.dataset.image;

    document.getElementById("productModal").style.display =
        "flex";
}

function closeModal() {

    document.getElementById("productModal").style.display =
        "none";
}

window.onclick = function (event) {

    const modal =
        document.getElementById("productModal");

    if (event.target === modal) {
        closeModal();
    }
}
