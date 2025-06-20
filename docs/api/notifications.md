### WebSocket Notifications System Documentation for Frontend Team

#### WebSocket Connection Details
**Endpoint URL:**
```text
{protocol}://{host}/ws/notifications/
```

| Component      | Development Value          | Production Value            |
|---------------|---------------------------|-------------------------------|
| Protocol      | `ws://`                   | `wss://`                      |
| Host          | `localhost:8000`          | `#TODO`                       |
| Full URL      | `ws://localhost:8000/ws/notifications/` | `#TODO`         |

---

#### Notification Data Structure
All notifications follow this JSON format:
```json
{
  "notification_id": 123,
  "notification_type": "REVIEW_LIKE",
  "message": "User123 liked your review of 'The Great Gatsby'",
  "payload": {
    "review_id": "c0a80121-7f5e-4d77-b9a2-93f8c7f1c4a3",
    "book_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "actor_id": "550e8400-e29b-41d4-a716-446655440000"
  },
  "timestamp": "2023-10-05T14:30:00Z",
  "is_read": false
}
```

**Key Fields:**
- `notification_id`: Unique notification identifier (integer)
- `notification_type`: One of these event types:
  - `REVIEW_LIKE`
  - `REVIEW_COMMENT`
  - `COMMENT_REPLY`
  - `FRIEND_ACTIVITY`
  - `BOOK_RECOMMENDATION`
- `message`: Human-readable notification text
- `payload`: Contextual data for navigation
- `timestamp`: ISO 8601 creation time
- `is_read`: Read status (boolean)

---

#### Payload Structures by Notification Type
| Type | Payload Fields | Description |
|------|----------------|-------------|
| **REVIEW_LIKE** | `review_id`, `book_id`, `actor_id` | User liked your review |
| **REVIEW_COMMENT** | `review_id`, `comment_id`, `book_id`, `actor_id` | New comment on your review |
| **COMMENT_REPLY** | `... #TODO` | Reply to your comment |
| **FRIEND_ACTIVITY** | `... #TODO` | Friend's reading activity |
| **BOOK_RECOMMENDATION** | `... #TODO` | Book recommendation from user |

---

#### Real-Time Updates
- Notifications are pushed immediately when events occur
- All connected devices receive the same notifications
- Auto-grouped by user ID (`notifications_{user_id}`)
- Guaranteed delivery order (FIFO per user)

---

#### Marking as Read
Javascript implementation (I have no idea how to implement this in Rust):
```js
socket.onopen = () => {

  function markSingleNotificationRead(notificationId) {
    socket.send(JSON.stringify({
      action: "mark_read",
      notification_id: notificationId
    }));
  }

};
```
