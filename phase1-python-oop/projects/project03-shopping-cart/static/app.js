// ============================================================
// ShopCart — Frontend JavaScript
// Talks to the Flask backend via fetch() API calls
// ============================================================

// --- State ---
let appliedCoupon = "";

// --- DOM helpers ---
const $ = id => document.getElementById(id);

// ============================================================
// 1. LOAD PRODUCTS — GET /api/products
// ============================================================
async function loadProducts() {
  const grid = $("products-grid");
  try {
    const res  = await fetch("/api/products");
    const data = await res.json();
    grid.innerHTML = "";
    data.forEach(p => {
      const hasDiscount = p.type === "DigitalProduct" && p.discount_pct > 0;
      const hasShipping = p.type === "PhysicalProduct" && p.shipping_cost > 0;
      grid.innerHTML += `
        <div class="product-card" id="card-${p.product_id}">
          <span class="product-category">${p.category}</span>
          <div class="product-name">${p.name}</div>
          <div class="product-type-tag">${p.type === "DigitalProduct" ? "Digital" : p.type === "PhysicalProduct" ? "Physical + Shipping" : "Standard"}</div>
          <div class="product-price-row">
            ${hasDiscount ? `<span class="product-base-price">Rs.${p.price}</span>` : ""}
            <span class="product-final-price">Rs.${p.final_price}</span>
            ${hasDiscount ? `<span class="product-discount-badge">${p.discount_pct}% OFF</span>` : ""}
            ${hasShipping ? `<span class="product-type-tag" style="font-size:0.7rem;color:#9494b8">+Rs.${p.shipping_cost} ship</span>` : ""}
          </div>
          <button class="btn-add-cart" id="addbtn-${p.product_id}" onclick="addToCart('${p.product_id}')">
            + Add to Cart
          </button>
        </div>`;
    });
  } catch(e) {
    grid.innerHTML = `<p style="color:var(--red);grid-column:1/-1;text-align:center;padding:3rem">Failed to load products. Is Flask running?</p>`;
  }
}

// ============================================================
// 2. ADD TO CART — POST /api/cart/add
// ============================================================
async function addToCart(productId) {
  const btn = $(`addbtn-${productId}`);
  btn.disabled = true;
  btn.textContent = "Adding...";

  const res  = await fetch("/api/cart/add", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: 1 })
  });
  const data = await res.json();

  if (data.success) {
    btn.textContent = "✓ Added";
    btn.classList.add("added");
    setTimeout(() => {
      btn.textContent = "+ Add to Cart";
      btn.classList.remove("added");
      btn.disabled = false;
    }, 1500);
    updateCartCount(data.cart_count);
    refreshCart();
  } else {
    btn.textContent = "Error";
    btn.disabled = false;
  }
}

// ============================================================
// 3. REFRESH CART — GET /api/cart
// ============================================================
async function refreshCart() {
  const res  = await fetch("/api/cart");
  const data = await res.json();
  renderCartItems(data.items);
  renderFinancials(data.financials);
  updateCartCount(data.cart_count);
}

// ============================================================
// 4. UPDATE QUANTITY — PUT /api/cart/update
// ============================================================
async function changeQuantity(productId, delta) {
  // First get current quantity from DOM
  const valEl = document.querySelector(`[data-qty-id="${productId}"]`);
  const currentQty = parseInt(valEl?.textContent || "1");
  const newQty = currentQty + delta;

  const res  = await fetch("/api/cart/update", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId, quantity: newQty })
  });
  const data = await res.json();
  renderCartItems(data.cart);
  refreshCart();
}

// ============================================================
// 5. REMOVE ITEM — DELETE /api/cart/remove
// ============================================================
async function removeItem(productId) {
  const res  = await fetch("/api/cart/remove", {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ product_id: productId })
  });
  const data = await res.json();
  refreshCart();
}

// ============================================================
// 6. APPLY COUPON (uses refreshCart which calls GET /api/cart)
// ============================================================
$("btn-apply-coupon").addEventListener("click", async () => {
  const code = $("coupon-input").value.trim();
  appliedCoupon = code;

  // ✅ FIX: pass the coupon code as a query param so Flask validates it
  const url  = code ? `/api/cart?coupon=${encodeURIComponent(code)}` : "/api/cart";
  const res  = await fetch(url);
  const data = await res.json();
  const fin  = data.financials;

  const msgEl = $("coupon-message");
  msgEl.textContent = fin.coupon_message;

  if (fin.discount > 0) {
    msgEl.className = "coupon-msg success";
  } else if (code) {
    msgEl.className = "coupon-msg error";
  } else {
    msgEl.className = "coupon-msg";
  }
  renderFinancials(fin);
});

// ============================================================
// 7. CHECKOUT — POST /api/cart/checkout
// ============================================================
$("btn-checkout").addEventListener("click", async () => {
  const couponCode    = $("coupon-input").value.trim() || null;
  const paymentMethod = $("payment-method").value;

  const res  = await fetch("/api/cart/checkout", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ coupon_code: couponCode, payment_method: paymentMethod })
  });
  const data = await res.json();

  if (data.success) {
    showOrderModal(data.receipt);
    refreshCart();
    $("coupon-input").value = "";
    $("coupon-message").textContent = "";
    appliedCoupon = "";
  } else {
    alert(data.message);
  }
});

// ============================================================
// RENDER HELPERS
// ============================================================

function renderCartItems(items) {
  const list = $("cart-items-list");

  if (!items || items.length === 0) {
    list.innerHTML = `<div class="cart-empty-state"><span class="empty-icon">🛒</span><p>Your cart is empty</p></div>`;
    $("financials-box").classList.add("hidden");
    $("btn-checkout").disabled = true;
    return;
  }

  $("btn-checkout").disabled = false;
  $("financials-box").classList.remove("hidden");

  list.innerHTML = items.map(item => `
    <div class="cart-item-row" id="row-${item.product_id}">
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-price">Rs.${item.unit_price} each &nbsp;|&nbsp; <strong style="color:var(--accent-2)">Rs.${item.subtotal}</strong></div>
      </div>
      <div class="cart-item-controls">
        <button class="qty-btn" onclick="changeQuantity('${item.product_id}', -1)">−</button>
        <span class="qty-val" data-qty-id="${item.product_id}">${item.quantity}</span>
        <button class="qty-btn" onclick="changeQuantity('${item.product_id}', 1)">+</button>
        <button class="remove-btn" onclick="removeItem('${item.product_id}')" title="Remove">✕</button>
      </div>
    </div>`).join("");
}

function renderFinancials(fin) {
  if (!fin) return;
  $("fin-subtotal").textContent = `Rs.${fin.subtotal}`;
  $("fin-discount").textContent = fin.discount > 0 ? `-Rs.${fin.discount}` : `-Rs.0`;
  $("fin-tax").textContent      = `Rs.${fin.tax}`;
  $("fin-total").textContent    = `Rs.${fin.final_total}`;
}

function updateCartCount(count) {
  $("cart-count-badge").textContent = count || 0;
}

function showOrderModal(receipt) {
  const fin = receipt.financials;
  $("modal-receipt").innerHTML = `
    <div><strong>Order ID:</strong> ${receipt.order_id}</div>
    <div><strong>Time:</strong> ${receipt.timestamp}</div>
    <div><strong>Payment:</strong> ${receipt.payment_method} — <span style="color:${receipt.payment_status==='PAID'?'var(--green)':'var(--accent-2)'}">${receipt.payment_status}</span></div>
    <div><strong>Items:</strong> ${receipt.items.join(", ")}</div>
    <div class="receipt-total">Total Paid: Rs.${fin.final_total} &nbsp; (incl. ${fin.discount > 0 ? `Rs.${fin.discount} discount + ` : ""}Rs.${fin.tax} tax)</div>`;
  $("order-modal").classList.remove("hidden");
}

// ============================================================
// CART SIDEBAR TOGGLE (mobile)
// ============================================================
$("btn-toggle-cart").addEventListener("click", () => {
  $("cart-sidebar").classList.toggle("open");
});
$("btn-close-cart").addEventListener("click", () => {
  $("cart-sidebar").classList.remove("open");
});
$("btn-close-modal").addEventListener("click", () => {
  $("order-modal").classList.add("hidden");
});

// ============================================================
// INIT
// ============================================================
loadProducts();
refreshCart();
