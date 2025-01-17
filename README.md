# Load Balancer Design Document

## Overview
The load balancer is designed to distribute client requests efficiently across multiple backend servers while ensuring high availability and reliability. It supports dynamic server registration and deregistration and uses a round-robin algorithm to route requests.

---

## Features

### Request Distribution
- **Round-Robin Algorithm**:
  - Distributes client requests evenly among available servers.
  - Ensures fair usage of resources.

### High Availability
- **Health Checks**:
  - A background task periodically verifies the health of servers by invoking their `/ping` endpoint.
  - Servers responding with non-2xx HTTP status codes are marked as unhealthy.
  - Unhealthy servers are excluded from the rotation until they recover.

### Dynamic Server Management
- **Registration**:
  - Servers register themselves using the `POST /urls/register_url` endpoint.
  - Requires service name and server URL as input.
- **De-registration**:
  - Servers can be removed from the load balancer using the `DELETE /urls/deregister_url` endpoint.

---

## Architecture

### Components
1. **Load Balancer Core**:
   - Routes requests to the appropriate server using the round-robin algorithm.
2. **Health Checker**:
   - Periodically checks the health of servers.
   - Updates the server status in real-time.
3. **In-Memory Key Store**:
   - Stores service-to-server mappings and server statuses.

### Data Flow
1. **Client Request**:
   - Incoming requests are intercepted by middleware.
   - The service name is extracted from the URL.
2. **Routing**:
   - The load balancer retrieves the list of servers for the requested service.
   - A server is selected using the round-robin algorithm.
   - The request is forwarded to the selected server.
3. **Health Checks**:
   - Runs periodically in the background.
   - Updates the status of servers based on `/ping` endpoint responses.

---

## API Endpoints

### Server Management
1. **Register Server**:
   - `POST /urls/register_url`
   - Payload: `{ "key": "service_name", "value": "http://server_url" }`
   - Adds a server to the load balancer.

2. **Deregister Server**:
   - `DELETE /urls/deregister_url`
   - Payload: `{ "key": "service_name", "value": "http://server_url" }`
   - Removes a server from the load balancer.

### Health Check
- **Ping Endpoint**:
  - `/ping`
  - Each server must implement this endpoint to report its health.

---

## Implementation Details

### Round-Robin Algorithm
- Uses a cycle iterator for each service.
- If a server becomes unhealthy, the algorithm skips it.
- If all servers are unhealthy, an exception is raised.

### Health Checker
- Runs at configurable intervals (e.g., every 30 seconds).
- Calls the `/ping` endpoint of each server.
- Updates the in-memory key store with server statuses.

### Middleware
- Intercepts all requests.
- Extracts the service name from the URL.
- Routes the request to the appropriate server or returns an error if no healthy servers are available.

---

## Conclusion
This load balancer is a foundational implementation that ensures fair request distribution, high availability, and flexibility for dynamic server management. With the outlined enhancements, it can evolve into a robust solution for large-scale distributed systems.
