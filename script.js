// Extended script.js with Admin Panel + Edit/Delete
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let customProducts = JSON.parse(localStorage.getItem('customProducts')) || [];

const baseProducts = [
    { name: 'T-Shirt', price: 15, imageUrl: 'images/1.webp', rating: 4 },
    { name: 'T-Shirt', price: 15, imageUrl: 'images/2.png', rating: 4 },
    { name: 'T-Shirt', price: 15, imageUrl: 'images/3.webp', rating: 4 },
    { name: 'Shirt', price: 20, imageUrl: 'images/4.avif', rating: 4 },
    { name: 'Shirt', price: 20, imageUrl: 'images/6.jpeg', rating: 4 },
    { name: 'Shirt', price: 20, imageUrl: 'images/7.avif', rating: 4 }
];

let currentSlide = 0;
let isEditing = false;
let editingIndex = -1;

function getAllProducts() {
    return [...baseProducts, ...customProducts];
}

document.addEventListener("DOMContentLoaded", () => {
    renderProducts();
    updateCartCount();
    displayCartItems();
    showSlide(currentSlide);
    updateUserUI();
});

function renderProducts(filtered = getAllProducts()) {
    const productGrid = document.getElementById('product-grid');
    productGrid.innerHTML = '';
    filtered.forEach((product, index) => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('product');
        productDiv.dataset.name = product.name;
        productDiv.dataset.price = product.price;

        const isCustom = index >= baseProducts.length;
        const customIndex = index - baseProducts.length;

        let adminControls = '';
        if (localStorage.getItem('loggedInUser')?.toLowerCase() === 'admin' && isCustom) {
            adminControls = `
                <button onclick="editProduct(${customIndex})">Edit</button>
                <button onclick="deleteProduct(${customIndex})">Delete</button>
            `;
        }

        productDiv.innerHTML = `
            <img src="${product.imageUrl}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p class="price">$${product.price}</p>
            <p>${'★'.repeat(product.rating)}${'☆'.repeat(5 - product.rating)}</p>
            <button onclick="addToCart('${product.name}')">Add to Cart</button>
            ${adminControls}
        `;
        productGrid.appendChild(productDiv);
    });
}

function addToCart(productName) {
    const product = getAllProducts().find(p => p.name === productName);
    if (product) {
        cart.push(product);
        saveCart();
        updateCartCount();
        displayCartItems();
    }
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.length;
}

function displayCartItems() {
    const cartItems = document.getElementById('cart-items');
    const totalDisplay = document.getElementById('total-price');
    cartItems.innerHTML = '';
    let total = 0;
    cart.forEach((product, index) => {
        total += product.price;
        const li = document.createElement('li');
        li.innerHTML = `
            <img src="${product.imageUrl}" alt="${product.name}" class="cart-image">
            ${product.name} - $${product.price}
            <button onclick="removeFromCart(${index})">Remove</button>
        `;
        cartItems.appendChild(li);
    });
    totalDisplay.textContent = `Total: $${total}`;
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    updateCartCount();
    displayCartItems();
}

function toggleCart() {
    document.getElementById('cart-modal').style.display = 'block';
}
function closeCheckout() {
    document.getElementById('checkout-modal').style.display = 'none';
}
function showCheckout() {
    const user = localStorage.getItem('loggedInUser');
    if (!user) {
        alert("Please login before checkout.");
        return;
    }
    document.getElementById('checkout-modal').style.display = 'block';
}
function submitOrder(event) {
    event.preventDefault();
    cart = [];
    saveCart();
    updateCartCount();
    displayCartItems();
    document.getElementById('order-status').textContent = 'Order placed successfully!';
    setTimeout(() => {
        closeCheckout();
        document.getElementById('order-status').textContent = '';
    }, 3000);
}

function showLogin() {
    document.getElementById('login-modal').style.display = 'block';
}
function hideLogin() {
    document.getElementById('login-modal').style.display = 'none';
}
function showRegister() {
    document.getElementById('register-modal').style.display = 'block';
}
function hideRegister() {
    document.getElementById('register-modal').style.display = 'none';
}
function loginUser(e) {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const users = JSON.parse(localStorage.getItem('users') || '{}');
    if (users[username] === password) {
        localStorage.setItem('loggedInUser', username);
        hideLogin();
        updateUserUI();
    } else {
        document.getElementById('login-status').textContent = 'Invalid credentials.';
    }
}
function registerUser(e) {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const users = JSON.parse(localStorage.getItem('users') || '{}');
    if (users[username]) {
        document.getElementById('register-status').textContent = 'Username already exists';
    } else {
        users[username] = password;
        localStorage.setItem('users', JSON.stringify(users));
        document.getElementById('register-status').textContent = 'Registered successfully. You can now login.';
    }
}
function updateUserUI() {
    const userArea = document.getElementById('user-area');
    const username = localStorage.getItem('loggedInUser');
    const adminButton = document.getElementById('admin-button');
    if (username) {
        userArea.innerHTML = `Welcome, ${username} | <a href="javascript:void(0);" onclick="logoutUser()">Logout</a>`;
        adminButton.style.display = username.toLowerCase() === 'admin' ? 'inline-block' : 'none';
    } else {
        userArea.innerHTML = `
            <a href="javascript:void(0);" onclick="showLogin()">Login</a> /
            <a href="javascript:void(0);" onclick="showRegister()">Register</a>
        `;
        adminButton.style.display = 'none';
    }
    renderProducts();
}
function logoutUser() {
    localStorage.removeItem('loggedInUser');
    updateUserUI();
    alert('You have been logged out.');
}

function toggleMenu() {
    document.getElementById('nav-list').classList.toggle('show');
}

function filterProducts() {
    const query = document.getElementById('search').value.toLowerCase();
    const filtered = getAllProducts().filter(p => p.name.toLowerCase().includes(query));
    renderProducts(filtered);
}
function sortProducts() {
    const sortValue = document.getElementById('sort').value;
    let sortedProducts = getAllProducts();
    if (sortValue === 'price-asc') sortedProducts.sort((a, b) => a.price - b.price);
    if (sortValue === 'price-desc') sortedProducts.sort((a, b) => b.price - a.price);
    renderProducts(sortedProducts);
}

// Admin Panel Logic
function toggleAdminPanel() {
    const modal = document.getElementById('admin-modal');
    modal.style.display = modal.style.display === 'block' ? 'none' : 'block';
    document.getElementById('admin-form').reset();
    isEditing = false;
    editingIndex = -1;
}

function addProduct(e) {
    e.preventDefault();
    const name = document.getElementById('admin-name').value;
    const price = parseFloat(document.getElementById('admin-price').value);
    const imageUrl = document.getElementById('admin-img').value;
    const rating = parseInt(document.getElementById('admin-rating').value);

    if (!name || !price || !imageUrl || !rating) return;

    const newProduct = { name, price, imageUrl, rating };

    if (isEditing) {
        customProducts[editingIndex] = newProduct;
    } else {
        customProducts.push(newProduct);
    }

    localStorage.setItem('customProducts', JSON.stringify(customProducts));
    renderProducts();
    document.getElementById('admin-form').reset();
    document.getElementById('admin-status').textContent = isEditing ? 'Product updated!' : 'Product added!';
    setTimeout(() => {
        document.getElementById('admin-status').textContent = '';
        toggleAdminPanel();
    }, 1500);
}

function editProduct(index) {
    const product = customProducts[index];
    document.getElementById('admin-name').value = product.name;
    document.getElementById('admin-price').value = product.price;
    document.getElementById('admin-img').value = product.imageUrl;
    document.getElementById('admin-rating').value = product.rating;
    isEditing = true;
    editingIndex = index;
    toggleAdminPanel();
}

function deleteProduct(index) {
    if (confirm("Are you sure you want to delete this product?")) {
        customProducts.splice(index, 1);
        localStorage.setItem('customProducts', JSON.stringify(customProducts));
        renderProducts();
    }
}

function showSlide(index) {
    const slides = document.querySelectorAll('.carousel .slide');
    slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
}
function nextSlide() {
    const slides = document.querySelectorAll('.carousel .slide');
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}
setInterval(nextSlide, 3000);
