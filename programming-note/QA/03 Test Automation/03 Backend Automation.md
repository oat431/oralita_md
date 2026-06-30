---
tags:
- programming
- qa
- testing
---

# 03 Backend Automation

Automated backend tests are fast, reliable, and run on every commit. The goal: catch regressions before they reach production.

---

## The Java Testing Stack

| Layer | Tool | Purpose |
|-------|------|---------|
| **Unit** | JUnit 5 + Mockito | Test single classes, mock dependencies |
| **Integration** | Spring Boot Test + TestContainers | Test with real DB, real API |
| **API** | RestAssured / MockMvc | Test HTTP layer |
| **Contract** | Spring Cloud Contract / Pact | Verify provider-consumer contracts |
| **Performance** | JMeter / k6 / Gatling | Load testing |

---

## JUnit 5 + Mockito

```java
@ExtendWith(MockitoExtension.class)
class OrderServiceTest {
    
    @Mock
    private OrderRepository repository;
    
    @Mock
    private PaymentClient paymentClient;
    
    @InjectMocks
    private OrderService orderService;
    
    @Test
    void shouldCreateOrderAndChargePayment() {
        // Given
        CreateOrderRequest request = new CreateOrderRequest("user-1", 
            List.of(new OrderItem("product-1", 2)));
        when(paymentClient.charge(any())).thenReturn(new PaymentResult("success"));
        when(repository.save(any())).thenReturn(sampleOrder());
        
        // When
        Order order = orderService.createOrder(request);
        
        // Then
        assertEquals("CONFIRMED", order.getStatus());
        verify(paymentClient).charge(any());
        verify(repository).save(any());
    }
    
    @Test
    void shouldFailWhenPaymentDeclined() {
        when(paymentClient.charge(any()))
            .thenThrow(new PaymentDeclinedException("Insufficient funds"));
        
        assertThrows(PaymentDeclinedException.class, () -> {
            orderService.createOrder(new CreateOrderRequest("user-1", List.of()));
        });
        
        verify(repository, never()).save(any());  // Never persisted
    }
}
```

---

## TestContainers — Real Dependencies

Spin up real PostgreSQL, Redis, Kafka in Docker for integration tests.

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryTest {
    
    @Container
    static PostgreSQLContainer<?> postgres = 
        new PostgreSQLContainer<>("postgres:16")
            .withDatabaseName("testdb")
            .withUsername("test")
            .withPassword("test");
    
    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
    
    @Autowired
    private OrderRepository repository;
    
    @Test
    void shouldPersistAndRetrieveOrder() {
        Order order = new Order("user-1", OrderStatus.PENDING);
        Order saved = repository.save(order);
        
        Optional<Order> found = repository.findById(saved.getId());
        assertTrue(found.isPresent());
        assertEquals(OrderStatus.PENDING, found.get().getStatus());
    }
}
```

---

## API Testing with MockMvc

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private OrderService orderService;
    
    @Test
    void shouldReturnOrder() throws Exception {
        when(orderService.findById("123")).thenReturn(sampleOrder());
        
        mockMvc.perform(get("/orders/123")
                .header("Authorization", "Bearer " + validJwt))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value("123"))
            .andExpect(jsonPath("$.status").value("CONFIRMED"));
    }
    
    @Test
    void shouldReturn404ForMissingOrder() throws Exception {
        when(orderService.findById("999"))
            .thenThrow(new OrderNotFoundException("999"));
        
        mockMvc.perform(get("/orders/999"))
            .andExpect(status().isNotFound());
    }
}
```

---

## Test Data Management

| Strategy | When |
|----------|------|
| **Factory methods** | Simple test data — `createSampleOrder()` |
| **Builder pattern** | Complex objects — `Order.builder().withStatus(CONFIRMED).build()` |
| **Object Mother** | Pre-built test fixtures for common scenarios |
| **Faker library** | Random but realistic data (Java Faker) |

---

## Sources

- JUnit 5 — https://junit.org/junit5/
- Mockito — https://site.mockito.org/
- TestContainers — https://testcontainers.com/
