(function () {
  const messagesContainer = document.getElementById('chatMessages');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');

  if (!messagesContainer || !form || !input) return;

  const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
  const wsUrl = wsScheme + '://' + window.location.host + '/ws/chat/' + CONVERSATION_ID + '/';
  let socket = null;
  let reconnectDelay = 1000;

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function appendMessage(data) {
    const isOwn = data.sender_id === CURRENT_USER_ID;
    const bubble = document.createElement('div');
    bubble.className = 'chat-bubble ' + (isOwn ? 'chat-bubble--own' : 'chat-bubble--other');

    let html = '';
    if (!isOwn) {
      html += '<span class="chat-bubble-sender">' + escapeHtml(data.sender_name) + '</span>';
    }
    html += '<p class="chat-bubble-content">' + escapeHtml(data.content) + '</p>';
    html += '<span class="chat-bubble-time">' + escapeHtml(data.timestamp) + '</span>';

    bubble.innerHTML = html;
    messagesContainer.appendChild(bubble);
    scrollToBottom();
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
      socket.send(JSON.stringify({ type: 'mark_read' }));
    };

    socket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      if (data.type === 'chat_message') {
        appendMessage(data);
        if (data.sender_id !== CURRENT_USER_ID) {
          socket.send(JSON.stringify({ type: 'mark_read' }));
        }
      }
    };

    socket.onclose = function () {
      setTimeout(function () {
        reconnectDelay = Math.min(reconnectDelay * 2, 30000);
        connect();
      }, reconnectDelay);
    };
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    const content = input.value.trim();
    if (!content || !socket || socket.readyState !== WebSocket.OPEN) return;

    socket.send(JSON.stringify({
      type: 'chat_message',
      content: content,
    }));
    input.value = '';
    input.focus();
  });

  scrollToBottom();
  connect();
})();
