# Task 3: Topic-Based Filtering

This directory contains the solution for **Task 3** of the Publish/Subscribe middleware assignment.

## Objective
Extend the Task 2 Pub/Sub implementation to include **Topic/Subject based filtering**. Messages sent by publishers are now strictly routed *only* to subscribers who are listening on the exact same topic.

## Features Implemented
* **New Handshake Protocol**: Clients now send both their Role and Topic in the initial handshake string when connecting to the server (e.g., `ROLE:PUBLISHER,TOPIC:WEATHER`).
* **Topic Dictionary Routing**: The server groups clients internally using a `defaultdict(list)` mapping `topic` strings to lists of socket connections.
* **Isolated Broadcasting**: When the server receives a message from a publisher on `TOPIC_A`, it looks up the socket list for `TOPIC_A` and routes the message exclusively to them, ensuring `TOPIC_B` subscribers are completely isolated from the traffic.
* **Topic Formatting**: Messages delivered to subscribers are prefixed with the topic for clarity (e.g., `[WEATHER] It is sunny today!`).

---

## How to Run

### 1. Start the Server
Open a terminal and start the routing server:
```bash
python3 server.py 5000
```

### 2. Start Subscribers on Different Topics
Open two new terminals to represent subscribers on different topics.

**Terminal 2 (Topic A):**
```bash
python3 client.py 127.0.0.1 5000 SUBSCRIBER SPORTS
```

**Terminal 3 (Topic B):**
```bash
python3 client.py 127.0.0.1 5000 SUBSCRIBER WEATHER
```

### 3. Start Publishers on Different Topics
Open two new terminals to represent publishers on those topics.

**Terminal 4 (Topic A):**
```bash
python3 client.py 127.0.0.1 5000 PUBLISHER SPORTS
```

**Terminal 5 (Topic B):**
```bash
python3 client.py 127.0.0.1 5000 PUBLISHER WEATHER
```

### 4. Test the Topic-Based Filtering
* Type a message in Terminal 4 (SPORTS publisher). You will see it appear **only** in Terminal 2 (SPORTS subscriber). Terminal 3 will remain unaffected.
* Type a message in Terminal 5 (WEATHER publisher). You will see it appear **only** in Terminal 3 (WEATHER subscriber).

### 5. Terminate
Type `terminate` in any client terminal to gracefully disconnect.
Press `Ctrl+C` in the server terminal to shut down the server.
