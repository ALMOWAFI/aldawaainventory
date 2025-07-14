# Smart Glasses API Specification

## Overview

This document defines the API specification for smart glasses integration with the pharmacy inventory management system. The API enables real-time alerts, notifications, and feedback to pharmacy staff wearing smart glasses.

## Base URL

```
https://your-smart-glasses-api.example.com
```

## Authentication

All requests require Bearer token authentication:

```
Authorization: Bearer {your_api_token}
```

## Endpoints

### 1. Send Alert to Specific Device

Send an alert to a specific smart glasses device.

```http
POST /alert/{deviceId}
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `deviceId` | string | Unique identifier for the smart glasses device |

#### Request Body

```json
{
  "alertType": "string",           // Required: Type of alert
  "message": "string",             // Required: Alert message text
  "productId": "string",           // Optional: Associated product ID
  "soundAlert": boolean,           // Optional: Enable sound alert (default: false)
  "vibrationPattern": "string",    // Optional: Vibration pattern
  "displayDuration": number,       // Optional: Display duration in milliseconds
  "backgroundColor": "string",     // Optional: Background color (hex)
  "textColor": "string",          // Optional: Text color (hex)
  "priority": "string"            // Optional: Alert priority level
}
```

#### Alert Types

| Type | Description | Recommended Settings |
|------|-------------|---------------------|
| `manual_review_required` | Expiry date couldn't be parsed | Sound: true, Vibration: short-long-short |
| `expired_product` | Product has expired | Sound: true, Vibration: urgent, Background: #FF0000 |
| `near_expiry` | Product expires soon | Sound: true, Vibration: gentle, Background: #FFA500 |
| `low_stock` | Stock level is low | Sound: false, Vibration: gentle |
| `reorder_alert` | Reorder needed | Sound: true, Vibration: short |

#### Vibration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| `short` | Single short pulse | Information alerts |
| `short-long-short` | Morse code pattern | Manual review required |
| `urgent` | Rapid continuous pulses | Critical alerts (expired products) |
| `gentle` | Soft, slow pulses | Warnings (near expiry) |
| `double` | Two quick pulses | Low stock alerts |

#### Response

```json
{
  "success": true,
  "messageId": "alert-12345",
  "deviceId": "glasses-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "status": "delivered"
}
```

### 2. Broadcast Alert to All Devices

Send an alert to all active smart glasses devices.

```http
POST /broadcast
```

#### Request Body

Same as individual device alert, but without `deviceId` parameter.

#### Response

```json
{
  "success": true,
  "messageId": "broadcast-12345",
  "devicesCount": 15,
  "deliveredCount": 14,
  "failedDevices": ["glasses-008"],
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### 3. Get Device Status

Check the status and capabilities of a specific device.

```http
GET /device/{deviceId}/status
```

#### Response

```json
{
  "deviceId": "glasses-001",
  "isOnline": true,
  "batteryLevel": 75,
  "lastSeen": "2024-01-15T10:25:00Z",
  "capabilities": {
    "soundAlert": true,
    "vibration": true,
    "colorDisplay": true,
    "camera": true
  },
  "currentUser": "pharmacist-001"
}
```

### 4. Get All Active Devices

List all active smart glasses devices.

```http
GET /devices
```

#### Response

```json
{
  "devices": [
    {
      "deviceId": "glasses-001",
      "isOnline": true,
      "batteryLevel": 75,
      "currentUser": "pharmacist-001"
    },
    {
      "deviceId": "glasses-002",
      "isOnline": false,
      "batteryLevel": 20,
      "currentUser": "pharmacist-002"
    }
  ],
  "totalDevices": 2,
  "onlineDevices": 1
}
```

### 5. Clear Alert

Clear an active alert from a device.

```http
DELETE /alert/{deviceId}/{messageId}
```

#### Response

```json
{
  "success": true,
  "messageId": "alert-12345",
  "deviceId": "glasses-001",
  "clearedAt": "2024-01-15T10:35:00Z"
}
```

### 6. Update Device Settings

Update alert preferences for a specific device.

```http
PUT /device/{deviceId}/settings
```

#### Request Body

```json
{
  "soundEnabled": true,
  "vibrationEnabled": true,
  "brightnessLevel": 80,
  "alertFrequency": "normal",
  "doNotDisturbHours": {
    "enabled": false,
    "startTime": "22:00",
    "endTime": "06:00"
  }
}
```

## Webhook Notifications (Optional)

If your smart glasses system supports webhooks, you can receive notifications about device events:

### Device Events

```http
POST /webhook/device-events
```

#### Event Types

```json
{
  "eventType": "device_connected|device_disconnected|alert_acknowledged|alert_dismissed",
  "deviceId": "glasses-001",
  "timestamp": "2024-01-15T10:30:00Z",
  "userId": "pharmacist-001",
  "additionalData": {
    "alertId": "alert-12345",
    "responseTime": 5.2
  }
}
```

## Error Responses

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `bad_request` | Invalid request parameters |
| 401 | `unauthorized` | Invalid or missing authentication |
| 404 | `device_not_found` | Device ID doesn't exist |
| 429 | `rate_limit_exceeded` | Too many requests |
| 503 | `device_offline` | Target device is offline |

#### Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "device_not_found",
    "message": "Device glasses-999 not found",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

## Rate Limits

- **Individual Device Alerts**: 60 requests per minute per device
- **Broadcast Alerts**: 10 requests per minute
- **Status Queries**: 100 requests per minute

## Best Practices

### 1. Alert Prioritization

```javascript
const alertPriorities = {
  'expired_product': 'high',
  'manual_review_required': 'high',
  'near_expiry': 'medium',
  'low_stock': 'low'
};
```

### 2. Alert Timing

- **Critical Alerts**: Immediate delivery
- **Warning Alerts**: Batch delivery every 30 seconds
- **Info Alerts**: Batch delivery every 2 minutes

### 3. Device Management

- Check device status before sending alerts
- Implement fallback notifications (email/SMS) if device is offline
- Respect "Do Not Disturb" settings

### 4. Alert Acknowledgment

```javascript
// Wait for user acknowledgment before sending next critical alert
const waitForAcknowledgment = async (alertId, timeout = 30000) => {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => {
      reject(new Error('Alert acknowledgment timeout'));
    }, timeout);
    
    // Listen for acknowledgment webhook
    onAcknowledgment(alertId, () => {
      clearTimeout(timer);
      resolve();
    });
  });
};
```

## Sample Implementation

### Node.js Client Example

```javascript
class SmartGlassesClient {
  constructor(baseUrl, apiToken) {
    this.baseUrl = baseUrl;
    this.apiToken = apiToken;
  }

  async sendAlert(deviceId, alertData) {
    const response = await fetch(`${this.baseUrl}/alert/${deviceId}`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(alertData)
    });

    if (!response.ok) {
      throw new Error(`Alert failed: ${response.status}`);
    }

    return response.json();
  }

  async broadcastAlert(alertData) {
    const response = await fetch(`${this.baseUrl}/broadcast`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(alertData)
    });

    return response.json();
  }

  async getDeviceStatus(deviceId) {
    const response = await fetch(`${this.baseUrl}/device/${deviceId}/status`, {
      headers: {
        'Authorization': `Bearer ${this.apiToken}`
      }
    });

    return response.json();
  }
}

// Usage example
const client = new SmartGlassesClient(
  'https://smart-glasses-api.example.com',
  'your-api-token'
);

// Send expired product alert
await client.sendAlert('glasses-001', {
  alertType: 'expired_product',
  message: 'CRITICAL: Product MED-001 expired 3 days ago',
  productId: 'MED-001',
  soundAlert: true,
  vibrationPattern: 'urgent',
  displayDuration: 15000,
  backgroundColor: '#FF0000'
});
```

## Testing

### Test Device

For development and testing, you can use a test device ID: `test-device-001`

### Test Endpoints

```bash
# Test alert
curl -X POST "https://smart-glasses-api.example.com/alert/test-device-001" \
  -H "Authorization: Bearer your-test-token" \
  -H "Content-Type: application/json" \
  -d '{
    "alertType": "test_alert",
    "message": "This is a test alert",
    "soundAlert": true,
    "displayDuration": 5000
  }'

# Test device status
curl "https://smart-glasses-api.example.com/device/test-device-001/status" \
  -H "Authorization: Bearer your-test-token"
```

This API specification provides a comprehensive foundation for integrating smart glasses with your pharmacy inventory management system. Customize the endpoints and parameters based on your specific smart glasses hardware and requirements. 