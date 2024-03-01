
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('input', function(e) {
        var searchTerm = e.target.value.toLowerCase();
        var products = document.querySelectorAll('.product');

        products.forEach(function(product) {
            var productName = product.querySelector('.product-title').textContent.toLowerCase();
            if (productName.includes(searchTerm)) {
                product.style.display = '';
            } else {
                product.style.display = 'none';
            }
        });
    });
});

function goBack() {
    if (document.referrer.indexOf(window.location.hostname) !== -1) {
        history.back();
    } else {
        window.location.href = '/'; // Перенаправление на главную страницу, если предыдущей страницы нет
    }
}


function redirectTo(url) {
    window.location.href = url;
}

        
        
        function scrollToTop() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }

        function scrollToProducts() {
            const productsSection = document.querySelector(".products");
            productsSection.scrollIntoView({
                behavior: "smooth"
            });
        }

        function scrollToContacts() {
            const footer = document.querySelector("footer");
            footer.scrollIntoView({
                behavior: "smooth"
            });
        }


        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
        
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        