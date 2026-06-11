document.addEventListener('DOMContentLoaded', function() {

  // Auto-dismiss alerts
  var alerts = document.querySelectorAll('.alert');
  alerts.forEach(function(alert) {
    setTimeout(function() {
      try {
        var bs = new bootstrap.Alert(alert);
        bs.close();
      } catch(e) {}
    }, 6000);
  });

  // Like post (feed)
  document.querySelectorAll('.like-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var postId = this.dataset.postId;
      var icon = this.querySelector('i');
      likePostAjax(postId, icon);
    });
  });

  // Save post (feed)
  document.querySelectorAll('.save-btn').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      var postId = this.dataset.postId;
      var icon = this.querySelector('i');
      savePostAjax(postId, icon);
    });
  });

  // Post options dropdown
  document.querySelectorAll('.post-options').forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.stopPropagation();
      var dropdown = this.nextElementSibling;
      closeAllDropdowns();
      if (dropdown) dropdown.style.display = 'block';
    });
  });

  document.addEventListener('click', function() {
    closeAllDropdowns();
  });

  function closeAllDropdowns() {
    document.querySelectorAll('.post-card .ig-dropdown').forEach(function(d) {
      d.style.display = 'none';
    });
  }

  // Story viewer hover effect
  document.querySelectorAll('.story-ring').forEach(function(ring) {
    ring.addEventListener('click', function() {
      var name = this.querySelector('.story-name').textContent;
      // Basic story viewer placeholder
      if (name !== 'Your Story') {
        console.log('Open story for:', name);
      }
    });
  });

  // Lazy load images
  if ('IntersectionObserver' in window) {
    var imgObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          var img = entry.target;
          if (img.dataset.src) {
            img.src = img.dataset.src;
            img.removeAttribute('data-src');
          }
          imgObserver.unobserve(img);
        }
      });
    });
    document.querySelectorAll('img[loading="lazy"]').forEach(function(img) {
      imgObserver.observe(img);
    });
  }
});

function likePostAjax(postId, iconEl) {
  fetch('/posts/' + postId + '/like/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCSRFToken() }
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if (iconEl) {
      iconEl.className = data.liked ? 'bi bi-heart-fill text-danger' : 'bi bi-heart';
      iconEl.classList.remove('heart-animate');
      void iconEl.offsetWidth;
      iconEl.classList.add('heart-animate');
    }
    var countEl = document.getElementById('likes-count-' + postId);
    if (countEl) {
      countEl.textContent = data.likes_count > 0
        ? data.likes_count + (data.likes_count === 1 ? ' like' : ' likes')
        : '';
    }
  });
}

function savePostAjax(postId, iconEl) {
  fetch('/posts/' + postId + '/save/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCSRFToken() }
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    if (iconEl) {
      iconEl.className = data.saved ? 'bi bi-bookmark-fill' : 'bi bi-bookmark';
    }
  });
}

function getCSRFToken() {
  var name = 'csrftoken';
  var match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : '';
}
