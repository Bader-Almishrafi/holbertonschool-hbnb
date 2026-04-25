document.addEventListener('DOMContentLoaded', () => {
  initializeLoginPage();
  initializeIndexPage();
  initializePlacePage();
  initializeAddReviewPage();
});

function initializeLoginPage() {
  const loginForm = document.getElementById('login-form');

  if (!loginForm) {
    return;
  }

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const errorMessage = document.getElementById('error-message');

    if (errorMessage) {
      errorMessage.textContent = '';
    }

    const email = emailInput.value.trim();
    const password = passwordInput.value;

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          email: email,
          password: password
        })
      });

      const data = await response.json();

      if (response.ok) {
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
      } else if (errorMessage) {
        errorMessage.textContent = data.error || 'Login failed';
      }
    } catch (error) {
      if (errorMessage) {
        errorMessage.textContent = 'Unable to connect to the server';
      }
    }
  });
}

function initializeIndexPage() {
  const placesList = document.getElementById('places-list');
  const priceFilter = document.getElementById('price-filter');
  const loginLink = document.getElementById('login-link');

  if (!placesList || !priceFilter) {
    return;
  }

  const token = getCookie('token');

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }

  loadPriceFilter(priceFilter);
  fetchPlaces(token);
}

function initializePlacePage() {
  const placeDetails = document.getElementById('place-details');
  const addReviewSection = document.getElementById('add-review');
  const addReviewLink = document.getElementById('add-review-link');
  const loginLink = document.getElementById('login-link');

  if (!placeDetails) {
    return;
  }

  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }

  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }

  if (!placeId) {
    placeDetails.innerHTML = '<p>Place ID not found.</p>';
    return;
  }

  if (addReviewLink) {
    addReviewLink.href = `add_review.html?id=${placeId}`;
  }

  fetchPlaceDetails(token, placeId);
}

function initializeAddReviewPage() {
  const reviewForm = document.getElementById('review-form');

  if (!reviewForm) {
    return;
  }

  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  const reviewMessage = document.getElementById('review-message');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    window.location.href = 'index.html';
    return;
  }

  if (loginLink) {
    loginLink.style.display = 'none';
  }

  if (!placeId) {
    if (reviewMessage) {
      reviewMessage.textContent = 'Place ID not found.';
    }
    return;
  }

  reviewForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const reviewText = document.getElementById('review-text').value.trim();
    const rating = Number(document.getElementById('rating').value);

    if (reviewMessage) {
      reviewMessage.textContent = '';
    }

    try {
      const response = await fetch('http://127.0.0.1:5000/api/v1/reviews/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          text: reviewText,
          rating: rating,
          place_id: placeId
        })
      });

      const data = await response.json();

      if (response.ok) {
        if (reviewMessage) {
          reviewMessage.textContent = 'Review submitted successfully!';
        }
        reviewForm.reset();
      } else {
        if (reviewMessage) {
          reviewMessage.textContent = data.error || 'Failed to submit review.';
        }
      }
    } catch (error) {
      if (reviewMessage) {
        reviewMessage.textContent = 'Unable to connect to the server.';
      }
    }
  });
}

function getCookie(name) {
  const cookies = document.cookie.split(';');

  for (let i = 0; i < cookies.length; i += 1) {
    const cookie = cookies[i].trim();

    if (cookie.startsWith(`${name}=`)) {
      return cookie.substring(name.length + 1);
    }
  }

  return null;
}

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

function loadPriceFilter(priceFilter) {
  priceFilter.innerHTML = `
    <option value="all">All</option>
    <option value="10">10</option>
    <option value="50">50</option>
    <option value="100">100</option>
  `;

  priceFilter.addEventListener('change', () => {
    filterPlacesByPrice(priceFilter.value);
  });
}

async function fetchPlaces(token) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error('Failed to fetch places');
    }

    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    const placesList = document.getElementById('places-list');
    if (placesList) {
      placesList.innerHTML = '<p>Unable to load places.</p>';
    }
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');

  if (!placesList) {
    return;
  }

  placesList.innerHTML = '';

  places.forEach((place) => {
    const placeCard = document.createElement('div');
    placeCard.className = 'place-card';
    placeCard.dataset.price = place.price;

    placeCard.innerHTML = `
      <h3>${place.title}</h3>
      <p>${place.description || 'No description available.'}</p>
      <p><strong>Price:</strong> $${place.price} / night</p>
      <p><strong>Location:</strong> ${place.latitude}, ${place.longitude}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(placeCard);
  });
}

function filterPlacesByPrice(selectedPrice) {
  const placeCards = document.querySelectorAll('.place-card');

  placeCards.forEach((card) => {
    const placePrice = Number(card.dataset.price);

    if (selectedPrice === 'all' || placePrice <= Number(selectedPrice)) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}

async function fetchPlaceDetails(token, placeId) {
  const headers = {};

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers: headers
    });

    if (!response.ok) {
      throw new Error('Failed to fetch place details');
    }

    const place = await response.json();
    displayPlaceDetails(place);
  } catch (error) {
    const placeDetails = document.getElementById('place-details');

    if (placeDetails) {
      placeDetails.innerHTML = '<p>Unable to load place details.</p>';
    }
  }
}

function displayPlaceDetails(place) {
  const placeDetails = document.getElementById('place-details');

  if (!placeDetails) {
    return;
  }

  const amenities = Array.isArray(place.amenities) && place.amenities.length > 0
    ? `<ul>${place.amenities.map((amenity) => `<li>${amenity.name || amenity}</li>`).join('')}</ul>`
    : '<p>No amenities available.</p>';

  const reviews = Array.isArray(place.reviews) && place.reviews.length > 0
    ? place.reviews.map((review) => `
        <div class="review-card">
          <p>${review.text || 'No comment'}</p>
          <p><strong>User:</strong> ${review.user_id || 'Anonymous'}</p>
          <p><strong>Rating:</strong> ${review.rating ?? 'N/A'}</p>
        </div>
      `).join('')
    : '<p>No reviews yet.</p>';

  placeDetails.innerHTML = `
    <div class="place-info">
      <h2>${place.title}</h2>
      <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
      <p><strong>Price:</strong> $${place.price} / night</p>
      <p><strong>Latitude:</strong> ${place.latitude}</p>
      <p><strong>Longitude:</strong> ${place.longitude}</p>
      <p><strong>Owner:</strong> ${place.owner_id || 'Unknown'}</p>
    </div>

    <div class="place-info">
      <h3>Amenities</h3>
      ${amenities}
    </div>

    <div class="place-info">
      <h3>Reviews</h3>
      ${reviews}
    </div>
  `;
}