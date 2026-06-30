---
tags:
- api
- programming
- protocols
---

# 02 WebSocket

REST is request-response. WebSocket is a persistent, bidirectional connection. Once opened, either side can send data at any time — no polling, no repeated handshakes.

---

## HTTP vs WebSocket

```
HTTP:                          WebSocket:
Client ──req──► Server         Client ◄──────► Server
Client ◄──res── Server         (persistent, bidirectional)
Client ──req──► Server         
Client ◄──res── Server         
(each request = new connection)
```

---

## The Handshake

WebSocket starts as an HTTP request, then upgrades:

```
Client:  GET /chat HTTP/1.1
         Upgrade: websocket
         Connection: Upgrade

Server:  HTTP/1.1 101 Switching Protocols
         Upgrade: websocket
         Connection: Upgrade
```

After the upgrade, the TCP connection stays open. Both sides can `send()` and `onMessage()`.

---

## When to Use WebSocket

| ✅ Use WebSocket | ❌ Don't Use WebSocket |
|-----------------|------------------------|
| Chat applications | Simple CRUD API |
| Live sports scores / stock tickers | Infrequent updates (use polling) |
| Collaborative editing (Google Docs) | One-time data fetch |
| Multiplayer games | File uploads |
| Real-time notifications | REST with caching |

---

## Spring Boot WebSocket (STOMP)

STOMP (Simple Text Oriented Messaging Protocol) sits on top of WebSocket for pub/sub messaging.

```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {
    
    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        config.enableSimpleBroker("/topic");     // Clients subscribe here
        config.setApplicationDestinationPrefixes("/app");  // Clients send here
    }
    
    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        registry.addEndpoint("/ws").setAllowedOrigins("*");
    }
}

@Controller
public class ChatController {
    
    @MessageMapping("/chat.send")
    @SendTo("/topic/public")
    public ChatMessage sendMessage(ChatMessage message) {
        return message;  // Broadcasts to all subscribers
    }
}
```

```javascript
// Client (JavaScript STOMP)
const client = Stomp.client('ws://localhost:8080/ws');
client.connect({}, () => {
    client.subscribe('/topic/public', (message) => {
        console.log(JSON.parse(message.body));
    });
    client.send('/app/chat.send', {}, JSON.stringify({
        sender: 'Alice',
        content: 'Hello!'
    }));
});
```

---

## Server-Sent Events (SSE) — The Lighter Alternative

If you only need **server → client** (not bidirectional), use SSE instead:

| | WebSocket | SSE |
|---|:--------:|:---:|
| Direction | Bidirectional | Server → Client only |
| Protocol | WebSocket (ws://) | HTTP |
| Reconnection | Manual | Built-in (`EventSource` auto-reconnects) |
| Binary data | ✅ | ❌ (text only) |

```javascript
// SSE Client — one-liner
const source = new EventSource('/api/events');
source.onmessage = (event) => console.log(event.data);
```

---

## Sources

- WebSocket RFC 6455 — https://datatracker.ietf.org/doc/html/rfc6455
- Spring WebSocket — https://docs.spring.io/spring-framework/docs/current/reference/html/web.html#websocket
- STOMP Protocol — https://stomp.github.io/
