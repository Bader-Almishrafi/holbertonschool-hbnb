const API_BASE = 'http://127.0.0.1:5000/api/v1';

document.addEventListener('DOMContentLoaded', () => {
  bindGlobalActions();
  hydrateNavigation();

  const page = document.body.dataset.page;
  if (page === 'home') initHomePage();
  if (page === 'login') initLoginPage();
  if (page === 'register') initRegisterPage();
  if (page === 'place') initPlacePage();
  if (page === 'bookings') initBookingsPage();
  if (page === 'my-places') initMyPlacesPage();
  if (page === 'admin') initAdminPage();
});

function bindGlobalActions() {
  document.querySelectorAll('#logout-btn').forEach((btn) => btn.addEventListener('click', logout));
}

function hydrateNavigation() {
  const token = getToken();
  const authLink = document.getElementById('auth-link');
  const logoutItem = document.getElementById('logout-item');
  const logoutBtn = document.getElementById('logout-btn');
  if (authLink) authLink.classList.toggle('d-none', !!token);
  if (logoutItem) logoutItem.classList.toggle('d-none', !token);
  if (logoutBtn && document.body.dataset.page === 'place') logoutBtn.classList.toggle('d-none', !token);
  if (token) fetchMe().then((me) => {
    const adminLink = document.getElementById('admin-nav-link');
    if (adminLink) adminLink.classList.toggle('d-none', !me.is_admin);
    if (authLink && me.user) authLink.textContent = me.user.full_name;
  }).catch(() => {});
}

async function api(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  let data = null;
  try { data = await response.json(); } catch { data = null; }
  if (!response.ok) throw new Error(data?.error || 'Request failed');
  return data;
}

function saveSession(accessToken, user) {
  localStorage.setItem('token', accessToken);
  localStorage.setItem('user', JSON.stringify(user));
}

function getToken() { return localStorage.getItem('token'); }
function getCurrentUser() { try { return JSON.parse(localStorage.getItem('user')); } catch { return null; } }
function logout() { localStorage.clear(); window.location.href = 'login.html'; }
async function fetchMe() { return api('/auth/me'); }
function qs(id) { return document.getElementById(id); }
function getIdFromQuery() { return new URLSearchParams(window.location.search).get('id'); }
function fmtMoney(value) { return `$${Number(value).toLocaleString()}`; }

async function initHomePage() {
  const searchBtn = qs('search-btn');
  searchBtn?.addEventListener('click', loadPlaces);
  await loadPlaces();
}

async function loadPlaces() {
  const q = qs('search-query')?.value?.trim() || '';
  const city = qs('search-city')?.value?.trim() || '';
  const maxPrice = qs('search-price')?.value?.trim() || '';
  const params = new URLSearchParams();
  if (q) params.set('q', q);
  if (city) params.set('city', city);
  if (maxPrice) params.set('max_price', maxPrice);
  const places = await api(`/places/${params.toString() ? `?${params.toString()}` : ''}`);
  const list = qs('places-list');
  list.innerHTML = places.map((place) => `
    <div class="col-lg-4 col-md-6">
      <div class="card place-card border-0 shadow-sm h-100 overflow-hidden">
        <img src="${place.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80'}" class="card-img-top" alt="${place.title}">
        <div class="card-body d-flex flex-column">
          <div class="d-flex justify-content-between align-items-start gap-2 mb-2">
            <div>
              <h3 class="h5 fw-bold mb-1">${place.title}</h3>
              <p class="text-muted small mb-0">${place.city}, ${place.country}</p>
            </div>
            <span class="badge rounded-pill rating-badge"><i class="bi bi-star-fill"></i> ${place.average_rating ?? 'New'}</span>
          </div>
          <p class="text-muted">${place.description || 'No description available.'}</p>
          <div class="mt-auto d-flex justify-content-between align-items-center">
            <div><strong>${fmtMoney(place.price)}</strong> <span class="text-muted">/ night</span></div>
            <a href="place.html?id=${place.id}" class="btn btn-danger">View details</a>
          </div>
        </div>
      </div>
    </div>
  `).join('');
}

function initLoginPage() {
  qs('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      const data = await api('/auth/login', { method: 'POST', body: JSON.stringify({ email: qs('email').value.trim(), password: qs('password').value }) });
      saveSession(data.access_token, data.user);
      window.location.href = 'index.html';
    } catch (error) {
      qs('error-message').textContent = error.message;
    }
  });
}

function initRegisterPage() {
  qs('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = qs('register-message');
    try {
      const data = await api('/auth/register', { method: 'POST', body: JSON.stringify({ first_name: qs('first_name').value.trim(), last_name: qs('last_name').value.trim(), email: qs('register_email').value.trim(), password: qs('register_password').value }) });
      saveSession(data.access_token, data.user);
      msg.className = 'small text-success mt-3';
      msg.textContent = 'Account created. Redirecting...';
      setTimeout(() => window.location.href = 'index.html', 900);
    } catch (error) {
      msg.className = 'small text-danger mt-3';
      msg.textContent = error.message;
    }
  });
}

async function initPlacePage() {
  const placeId = getIdFromQuery();
  if (!placeId) return;
  const place = await api(`/places/${placeId}`);
  const token = getToken();
  const isLoggedIn = !!token;
  const details = qs('place-details');
  details.innerHTML = `
    <div class="row g-4">
      <div class="col-lg-7"><img src="${place.image_url || 'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=80'}" class="img-fluid rounded-4 shadow-sm place-cover w-100" alt="${place.title}"></div>
      <div class="col-lg-5">
        <div class="card border-0 shadow-sm rounded-4 h-100"><div class="card-body p-4">
          <div class="d-flex justify-content-between align-items-start mb-3"><div><h1 class="h2 fw-bold mb-1">${place.title}</h1><p class="text-muted mb-0">${place.city}, ${place.country} • Hosted by ${place.owner_name}</p></div><span class="badge rating-badge rounded-pill"><i class="bi bi-star-fill"></i> ${place.average_rating ?? 'New'}</span></div>
          <p class="text-muted">${place.description || 'No description available.'}</p>
          <div class="row g-3 small mb-4"><div class="col-6"><div class="p-3 bg-light rounded-3"><strong>${fmtMoney(place.price)}</strong><br><span class="text-muted">per night</span></div></div><div class="col-6"><div class="p-3 bg-light rounded-3"><strong>${place.max_guests}</strong><br><span class="text-muted">max guests</span></div></div></div>
          <h2 class="h6 fw-bold">Amenities</h2>
          <div class="d-flex flex-wrap gap-2 mb-4">${place.amenities.map((a) => `<span class="badge text-bg-light border">${a.name}</span>`).join('') || '<span class="text-muted">No amenities listed</span>'}</div>
          ${isLoggedIn ? `
          <form id="booking-form" class="border rounded-4 p-3 bg-light-subtle">
            <h2 class="h6 fw-bold">Reserve this stay</h2>
            <div class="row g-2"><div class="col-6"><label class="form-label small">Check in</label><input id="check_in_date" type="date" class="form-control" required></div><div class="col-6"><label class="form-label small">Check out</label><input id="check_out_date" type="date" class="form-control" required></div><div class="col-12"><label class="form-label small">Guests</label><input id="booking_guests" type="number" min="1" max="${place.max_guests}" value="1" class="form-control" required></div></div>
            <button class="btn btn-danger w-100 mt-3">Book now</button><div id="booking-message" class="small mt-3"></div>
          </form>
          <form id="review-form" class="border rounded-4 p-3 mt-3">
            <h2 class="h6 fw-bold">Leave a review</h2>
            <textarea id="review-text" class="form-control mb-2" rows="3" placeholder="Share your experience"></textarea>
            <select id="review-rating" class="form-select mb-2"><option value="5">5 stars</option><option value="4">4 stars</option><option value="3">3 stars</option><option value="2">2 stars</option><option value="1">1 star</option></select>
            <button class="btn btn-outline-danger w-100">Submit review</button><div id="review-message" class="small mt-3"></div>
          </form>` : `<a href="login.html" class="btn btn-danger w-100">Login to book or review</a>`}
        </div></div>
      </div>
    </div>
    <section class="mt-5"><h2 class="h4 fw-bold mb-3">Guest reviews</h2><div class="row g-3">${(place.reviews || []).map((review) => `<div class="col-lg-6"><div class="card border-0 shadow-sm h-100"><div class="card-body"><div class="d-flex justify-content-between"><strong>${review.user_name}</strong><span class="badge rating-badge rounded-pill">${review.rating}/5</span></div><p class="text-muted small mt-2 mb-0">${review.text}</p></div></div></div>`).join('') || '<p class="text-muted">No reviews yet.</p>'}</div></section>
  `;
  qs('booking-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = qs('booking-message');
    try {
      await api('/bookings/', { method: 'POST', body: JSON.stringify({ place_id: place.id, check_in_date: qs('check_in_date').value, check_out_date: qs('check_out_date').value, guests: Number(qs('booking_guests').value) }) });
      msg.className = 'small text-success mt-3'; msg.textContent = 'Booking created successfully.';
    } catch (error) { msg.className = 'small text-danger mt-3'; msg.textContent = error.message; }
  });
  qs('review-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = qs('review-message');
    try {
      await api('/reviews/', { method: 'POST', body: JSON.stringify({ place_id: place.id, text: qs('review-text').value.trim(), rating: Number(qs('review-rating').value) }) });
      msg.className = 'small text-success mt-3'; msg.textContent = 'Review submitted. Refreshing...';
      setTimeout(() => location.reload(), 700);
    } catch (error) { msg.className = 'small text-danger mt-3'; msg.textContent = error.message; }
  });
}

async function initBookingsPage() {
  if (!getToken()) return window.location.href = 'login.html';
  const bookings = await api('/bookings/my-bookings');
  qs('bookings-list').innerHTML = bookings.map((booking) => `
    <div class="col-lg-6"><div class="card border-0 shadow-sm rounded-4 h-100"><div class="card-body">
      <div class="d-flex justify-content-between align-items-start mb-3"><div><h2 class="h5 fw-bold mb-1">${booking.place_title}</h2><p class="text-muted small mb-0">${booking.check_in_date} → ${booking.check_out_date}</p></div><span class="badge ${booking.status === 'confirmed' ? 'text-bg-success' : booking.status === 'cancelled' ? 'text-bg-secondary' : 'text-bg-warning'}">${booking.status}</span></div>
      <p class="mb-2"><strong>Total:</strong> ${fmtMoney(booking.total_price)}</p><p class="mb-3"><strong>Guests:</strong> ${booking.guests}</p>
      ${booking.status !== 'cancelled' ? `<button class="btn btn-outline-danger" onclick="cancelBooking('${booking.id}')">Cancel booking</button>` : ''}
    </div></div></div>
  `).join('') || '<p class="text-muted">No bookings found yet.</p>';
}

async function cancelBooking(id) {
  await api(`/bookings/${id}`, { method: 'DELETE' });
  location.reload();
}
window.cancelBooking = cancelBooking;

async function initMyPlacesPage() {
  if (!getToken()) return window.location.href = 'login.html';
  const me = await fetchMe();
  const allPlaces = await api('/places/');
  renderMyPlaces(allPlaces.filter((place) => place.owner_id === me.user.id));
  qs('place-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const msg = qs('place-message');
    try {
      await api('/places/', { method: 'POST', body: JSON.stringify({ title: qs('place_title').value.trim(), description: qs('place_description').value.trim(), price: Number(qs('place_price').value), max_guests: Number(qs('place_guests').value), city: qs('place_city').value.trim(), country: qs('place_country').value.trim(), latitude: Number(qs('place_latitude').value), longitude: Number(qs('place_longitude').value), image_url: qs('place_image_url').value.trim(), amenities: [] }) });
      msg.className = 'small text-success mt-3'; msg.textContent = 'Place created successfully.';
      setTimeout(() => location.reload(), 700);
    } catch (error) { msg.className = 'small text-danger mt-3'; msg.textContent = error.message; }
  });
}

function renderMyPlaces(places) {
  qs('my-places-list').innerHTML = places.map((place) => `
    <div class="col-md-6"><div class="card border-0 shadow-sm rounded-4 overflow-hidden h-100"><img src="${place.image_url || 'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=1200&q=80'}" class="card-img-top place-card-image" alt="${place.title}"><div class="card-body"><h3 class="h5 fw-bold">${place.title}</h3><p class="text-muted small">${place.city}, ${place.country}</p><p class="text-muted">${place.description || 'No description available.'}</p><div class="d-flex justify-content-between align-items-center"><span><strong>${fmtMoney(place.price)}</strong> / night</span><a class="btn btn-outline-danger btn-sm" href="place.html?id=${place.id}">View</a></div></div></div></div>
  `).join('') || '<p class="text-muted">You have not created any places yet.</p>';
}

async function initAdminPage() {
  if (!getToken()) return window.location.href = 'login.html';
  const me = await fetchMe();
  if (!me.is_admin) return window.location.href = 'index.html';
  const [stats, users, bookings, places] = await Promise.all([api('/admin/stats'), api('/admin/users'), api('/admin/bookings'), api('/admin/places')]);
  qs('admin-stats').innerHTML = [
    ['Users', stats.users], ['Places', stats.places], ['Bookings', stats.bookings], ['Reviews', stats.reviews], ['Revenue', fmtMoney(stats.revenue)], ['Cancelled', stats.cancelled_bookings]
  ].map(([label, value]) => `<div class="col-md-4 col-xl-2"><div class="card dashboard-stat"><div class="card-body"><div class="text-muted small">${label}</div><div class="h4 fw-bold mb-0">${value}</div></div></div></div>`).join('');
  qs('admin-users-table').innerHTML = `<thead><tr><th>Name</th><th>Email</th><th>Role</th></tr></thead><tbody>${users.slice(0, 10).map((user) => `<tr><td>${user.full_name}</td><td>${user.email}</td><td>${user.is_admin ? 'Admin' : 'User'}</td></tr>`).join('')}</tbody>`;
  qs('admin-bookings-table').innerHTML = `<thead><tr><th>Guest</th><th>Place</th><th>Status</th></tr></thead><tbody>${bookings.slice(0, 10).map((booking) => `<tr><td>${booking.user_name}</td><td>${booking.place_title}</td><td><span class="badge ${booking.status === 'confirmed' ? 'text-bg-success' : booking.status === 'cancelled' ? 'text-bg-secondary' : 'text-bg-warning'}">${booking.status}</span></td></tr>`).join('')}</tbody>`;
  renderAdminCharts(bookings, places);
}

function renderAdminCharts(bookings, places) {
  if (typeof Chart === 'undefined') return;

  const statusCounts = bookings.reduce((acc, booking) => {
    acc[booking.status] = (acc[booking.status] || 0) + 1;
    return acc;
  }, { confirmed: 0, pending: 0, cancelled: 0 });

  const revenueByMonth = bookings
    .filter((booking) => booking.status === 'confirmed')
    .reduce((acc, booking) => {
      const key = booking.check_in_date.slice(0, 7);
      acc[key] = (acc[key] || 0) + Number(booking.total_price || 0);
      return acc;
    }, {});

  const cityCounts = places.reduce((acc, place) => {
    acc[place.city] = (acc[place.city] || 0) + 1;
    return acc;
  }, {});

  const revenueLabels = Object.keys(revenueByMonth).sort();
  const topCities = Object.entries(cityCounts).sort((a, b) => b[1] - a[1]).slice(0, 6);

  new Chart(qs('booking-status-chart'), {
    type: 'doughnut',
    data: {
      labels: ['Confirmed', 'Pending', 'Cancelled'],
      datasets: [{ data: [statusCounts.confirmed || 0, statusCounts.pending || 0, statusCounts.cancelled || 0], borderWidth: 0 }]
    },
    options: { plugins: { legend: { position: 'bottom' } } }
  });

  new Chart(qs('monthly-revenue-chart'), {
    type: 'bar',
    data: {
      labels: revenueLabels,
      datasets: [{ label: 'Revenue', data: revenueLabels.map((label) => Math.round(revenueByMonth[label])) }]
    },
    options: { scales: { y: { beginAtZero: true } }, plugins: { legend: { display: false } } }
  });

  new Chart(qs('top-cities-chart'), {
    type: 'bar',
    data: {
      labels: topCities.map(([city]) => city),
      datasets: [{ label: 'Listings', data: topCities.map(([, count]) => count) }]
    },
    options: { indexAxis: 'y', scales: { x: { beginAtZero: true, ticks: { precision: 0 } } }, plugins: { legend: { display: false } } }
  });
}
