(function () {
  const badge = document.getElementById('inboxBadge');
  if (!badge) return;

  const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsUrl = wsScheme + '://' + window.location.host + '/ws/notifications/';
  let socket = null;
  let reconnectDelay = 1000;

  function updateBadge(count) {
    if (count > 0) {
      badge.textContent = count > 99 ? '99+' : count;
      badge.style.display = 'flex';
    } else {
      badge.textContent = '';
      badge.style.display = 'none';
    }
  }

  function showToast(senderName, preview) {
    const existing = document.querySelector('.chat-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'chat-toast';
    toast.innerHTML =
      '<strong>' + escapeHtml(senderName) + '</strong>' +
      '<p>' + escapeHtml(preview) + '</p>';
    document.body.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add('chat-toast--visible');
    });

    setTimeout(function () {
      toast.classList.remove('chat-toast--visible');
      setTimeout(function () { toast.remove(); }, 300);
    }, 4000);
  }

  function playNotificationSound() {
    try {
      var ctx = new (window.AudioContext || window.webkitAudioContext)();
      var now = ctx.currentTime;

      // Two-tone chime: C5 then E5
      var frequencies = [523.25, 659.25];
      frequencies.forEach(function (freq, i) {
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        gain.gain.setValueAtTime(0.18, now + i * 0.12);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.12 + 0.25);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now + i * 0.12);
        osc.stop(now + i * 0.12 + 0.25);
      });
    } catch (e) {
      // AudioContext blocked until user interaction — safe to ignore
    }
  }

  function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  function connect() {
    socket = new WebSocket(wsUrl);

    socket.onopen = function () {
      reconnectDelay = 1000;
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);

      if (data.type === 'unread_count') {
        updateBadge(data.count);
      } else if (data.type === 'new_message') {
        updateBadge(data.unread_count);
        showToast(data.sender_name, data.preview);
        playNotificationSound();
      }
    };

    socket.onclose = function () {
      setTimeout(function () {
        reconnectDelay = Math.min(reconnectDelay * 2, 30000);
        connect();
      }, reconnectDelay);
    };
  }

  connect();
})();
