const PRODUCTS_PER_PAGE =
    window.innerWidth <= 768 ? 4 : 8;

const cards =
    document.querySelectorAll(".card");

cards.forEach((card, index) => {

    const page =
        Math.floor(index / PRODUCTS_PER_PAGE);

    card.dataset.page = page;
});

let currentPage = 0;

const totalPages =
    Math.ceil(cards.length / PRODUCTS_PER_PAGE);

function buildDots() {

    const dotsContainer =
        document.getElementById("galleryDots");

    dotsContainer.innerHTML = "";

    for (let i = 0; i < totalPages; i++) {

        const dot =
            document.createElement("div");

        dot.classList.add("dot");

        if (i === currentPage) {
            dot.classList.add("active");
        }

        dotsContainer.appendChild(dot);
    }
}

function updateDots() {

    const dots =
        document.querySelectorAll(".dot");

    dots.forEach((dot, index) => {

        dot.classList.toggle(
            "active",
            index === currentPage
        );

    });
}

let indicatorTimer;
function showIndicator() {

    const indicator =
        document.getElementById("pageIndicator");

    indicator.innerText =
        `${currentPage + 1} / ${totalPages}`;

    indicator.style.opacity = "1";

    clearTimeout(indicatorTimer);

    indicatorTimer = setTimeout(() => {

        indicator.style.opacity = "0";

    }, 800);
}

function showPage(pageNumber) {

    const productsGrid =
        document.getElementById("productsGrid");

    productsGrid.classList.add("fading");

    setTimeout(() => {

        cards.forEach(card => {

            if (Number(card.dataset.page) === pageNumber) {

                card.style.display = "";

            } else {

                card.style.display = "none";
            }

        });

        currentPage = pageNumber;

        updateDots();
        showIndicator();

        productsGrid.classList.remove("fading");

    }, 180);
}

buildDots();

showPage(0);
function nextPage() {

    if (currentPage < totalPages - 1) {

        showPage(currentPage + 1);

    }
}

function previousPage() {

    if (currentPage > 0) {

        showPage(currentPage - 1);

    }
}
let wheelLocked = false;

const gallery =
    document.querySelector(".gallery-container");

gallery.addEventListener("wheel", function (event) {

    event.preventDefault();

    if (wheelLocked) {
        return;
    }

    wheelLocked = true;

    setTimeout(() => {

        wheelLocked = false;

    }, 500);

    if (Math.abs(event.deltaY) < 50) {
        return;
    }

    if (event.deltaY > 0) {

        nextPage();

    } else {

        previousPage();

    }

}, { passive: false });

// This line of code below stops the page from reloading and also controls the added to cart notification. 
async function addToCart(productId) {

    const response =
        await fetch(`/api/add_to_cart/${productId}`);

    const data =
        await response.json();

    if (data.success) {

        document.getElementById("cart-link").innerText =
            `Cart (${data.cart_count})`;

        const toast =
            document.getElementById("cart-toast");

        toast.classList.add("show");

        setTimeout(() => {
            toast.classList.remove("show");
        }, 2000);
    }
}

let startY = 0;

gallery.addEventListener("touchstart", (e) => {
    startY = e.touches[0].clientY;
});

gallery.addEventListener("touchend", (e) => {
    const endY = e.changedTouches[0].clientY;
    const distance = startY - endY;

    if (Math.abs(distance) < 50) return;

    if (distance > 0) {
        nextPage();
    } else {
        previousPage();
    }
});