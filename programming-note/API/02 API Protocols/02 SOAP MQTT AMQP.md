# 02 SOAP, MQTT & AMQP

Three additional protocols from the original API note. SOAP is legacy enterprise, MQTT is IoT-focused, AMQP is a messaging wire protocol — none are first-choice for new projects but all still appear in production.

---

## SOAP (Simple Object Access Protocol)

The enterprise grandfather of API protocols. XML-only, rigid, heavily specified.

| | SOAP | REST |
|---|------|------|
| **Format** | XML only | JSON, XML, anything |
| **Contract** | WSDL (mandatory) | OpenAPI (optional) |
| **Transport** | HTTP, SMTP, TCP, JMS | HTTP/HTTPS |
| **Error handling** | Built-in `<fault>` element | HTTP status codes |
| **State** | Supports stateful operations | Stateless |
| **Tooling** | Heavy (WSDL → code gen required) | Light |
| **Still used?** | Banks, payment gateways, legacy enterprise | Everything else |

```xml
<!-- SOAP Request -->
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">
  <soap:Header>
    <auth:Token>abc123</auth:Token>
  </soap:Header>
  <soap:Body>
    <GetOrder xmlns="http://example.com/orders">
      <OrderId>123</OrderId>
    </GetOrder>
  </soap:Body>
</soap:Envelope>
```

> **When you'll encounter it:** Integrating with older banking systems, payment gateways, or enterprise SAP/Oracle systems. Learn enough to consume SOAP APIs — don't build new ones with it.

---

## MQTT (Message Queue Telemetry Transport)

Lightweight pub/sub protocol designed for IoT — low bandwidth, low power, unreliable networks.

| | MQTT | HTTP |
|---|------|------|
| **Model** | Publish/Subscribe | Request/Response |
| **Overhead** | 2-byte minimum header | Headers can be kilobytes |
| **Connection** | Persistent TCP | Per-request TCP |
| **QoS Levels** | 0 (at most once), 1 (at least once), 2 (exactly once) | None built-in |
| **Best for** | IoT sensors, mobile push, telemetry | Web APIs |

```
MQTT Broker
  ├── Sensor 1 → publish("temperature", 23.5)
  ├── Sensor 2 → publish("humidity", 60)
  ├── Dashboard → subscribe("temperature")
  └── Alert Svc → subscribe("temperature")
```

> **When to use:** IoT devices, mobile push notifications (Facebook Messenger uses MQTT), any scenario with thousands of lightweight clients and unreliable networks.

---

## AMQP (Advanced Message Queuing Protocol)

Wire-level protocol for message-oriented middleware. Unlike MQTT (IoT) and HTTP (web), AMQP is designed for reliable enterprise messaging.

| | AMQP (RabbitMQ) | Kafka |
|---|:---:|:---:|
| **Model** | Queues + Exchanges + Bindings | Distributed log |
| **Routing** | Flexible (topic, direct, fanout, headers) | Topic-based |
| **Message ack** | Per-message | Per-offset (consumer group) |
| **Replay** | ❌ | ✅ |
| **Best for** | Task queues, RPC, work distribution | Event streaming, audit, analytics |

```
Producer → Exchange → [binding rules] → Queue → Consumer
                      ↓
                 Another Queue → Another Consumer
```

> **When to use:** Background job processing, task queues, microservice communication where you need flexible routing and per-message acknowledgments. RabbitMQ is the most common AMQP broker.

---

## Quick Comparison

| | SOAP | MQTT | AMQP |
|---|:---:|:---:|:---:|
| **Era** | 1998 | 1999 | 2003 |
| **Primary use** | Enterprise web services | IoT, telemetry | Enterprise messaging |
| **Message size** | Large (XML) | Tiny (binary) | Medium |
| **Learning curve** | High (WSDL, tooling) | Low | Medium |
| **Use in new projects** | Rarely | IoT only | For message broker backends |

---

## Sources

- SOAP 1.2 — https://www.w3.org/TR/soap12/
- MQTT 5.0 — https://mqtt.org/
- AMQP 1.0 — https://www.amqp.org/
