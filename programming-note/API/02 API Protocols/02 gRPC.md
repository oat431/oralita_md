# 02 gRPC

gRPC is a high-performance RPC framework from Google. It uses Protocol Buffers for serialization and HTTP/2 for transport — making it dramatically faster and smaller than REST/JSON for service-to-service communication.

---

## REST vs gRPC

| | REST | gRPC |
|---|------|------|
| **Data format** | JSON (text) | Protobuf (binary) |
| **Transport** | HTTP/1.1 | HTTP/2 |
| **Contract** | OpenAPI (optional) | `.proto` file (required) |
| **Speed** | Good | 3–10x faster, smaller payload |
| **Streaming** | No (SSE is hack) | Native: unary, server, client, bidirectional |
| **Browser support** | Native | Requires gRPC-Web proxy |
| **Code generation** | Optional (OpenAPI Generator) | Built-in (`protoc`) |

---

## Protocol Buffers (.proto)

Define your service and messages once. Generate client and server code in 10+ languages.

```protobuf
syntax = "proto3";

package order;

service OrderService {
  rpc GetOrder (GetOrderRequest) returns (Order);
  rpc ListOrders (ListOrdersRequest) returns (ListOrdersResponse);
  rpc CreateOrder (CreateOrderRequest) returns (Order);
  rpc WatchOrderStatus (WatchOrderRequest) returns (stream OrderStatus);
}

message Order {
  string id = 1;
  string user_id = 2;
  OrderStatus status = 3;
  repeated OrderItem items = 4;
  int64 total_cents = 5;
}

message GetOrderRequest {
  string order_id = 1;
}

message CreateOrderRequest {
  string user_id = 1;
  repeated OrderItem items = 2;
}

enum OrderStatus {
  PENDING = 0;
  CONFIRMED = 1;
  SHIPPED = 2;
  CANCELLED = 3;
}
```

---

## Streaming Modes

| Mode | Description | Use Case |
|------|------------|----------|
| **Unary** | 1 request → 1 response | Standard API call |
| **Server streaming** | 1 request → many responses | Real-time updates, log tailing |
| **Client streaming** | many requests → 1 response | File upload, sensor data |
| **Bidirectional** | many ↔ many | Chat, gaming, real-time collaboration |

```protobuf
// Bidirectional streaming
rpc Chat(stream ChatMessage) returns (stream ChatMessage);
```

---

## Spring Boot + gRPC

```java
// Server implementation
@GrpcService
public class OrderServiceImpl extends OrderServiceGrpc.OrderServiceImplBase {
    
    @Override
    public void getOrder(GetOrderRequest request, 
                         StreamObserver<Order> responseObserver) {
        Order order = orderService.findById(request.getOrderId());
        responseObserver.onNext(order);
        responseObserver.onCompleted();
    }
}
```

```yaml
# Client configuration
grpc:
  client:
    order-service:
      address: static://order-service:9090
      negotiationType: plaintext
```

---

## When to Use gRPC

| ✅ Use gRPC | ❌ Don't Use gRPC |
|------------|------------------|
| Microservice-to-microservice | Browser-to-server (use gRPC-Web or REST) |
| High throughput, low latency needed | Simple CRUD for mobile/web clients |
| Polyglot environments (Java, Go, Python services) | Public API (REST is more accessible) |
| Streaming data | Request-response is fine |

---

## Sources

- gRPC — https://grpc.io/
- Protocol Buffers — https://protobuf.dev/
- gRPC-Spring-Boot-Starter — https://github.com/yidongnan/grpc-spring-boot-starter
