# Pharmacy Inventory Management n8n Workflow

## Overview

This comprehensive n8n workflow automates pharmacy inventory management with real-time scanning, expiry date validation, smart alerts, and automated reporting. It's designed to work with smart glasses, mobile devices, and integrate with existing ERP systems.

## Key Features

### 🔍 Real-time Inventory Scanning
- Webhook endpoint for receiving scan data from smart glasses or mobile devices
- Support for product ID, quantity, raw expiry date text, and optional image URLs
- Device identification and tracking

### 📅 Advanced Expiry Date Parsing
- Supports multiple date formats (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD, MM/YY, etc.)
- Handles text formats like "EXP 12/24", "BEST BY 01/25"
- Intelligent 2-digit year handling
- Robust error handling for unparseable dates

### ⚠️ Smart Alerting System
- **Critical Alerts**: Expired products and unparseable expiry dates
- **Warning Alerts**: Products expiring within 30 days
- **Procurement Alerts**: Low stock level notifications
- **Multi-channel**: Smart glasses, email, Slack integration

### 🏥 Smart Glasses Integration
- Real-time visual and audio alerts
- Different alert patterns for different scenarios
- Sound alerts with vibration patterns
- Customizable display duration and colors

### 📊 Comprehensive Reporting
- Weekly automated reports
- Inventory statistics and trends
- Quality metrics and device usage analytics
- HTML email reports with detailed insights

### 🔐 Audit & Compliance
- Complete activity logging
- Traceability for all scans and updates
- Compliance-ready audit trails

## Setup Instructions

### 1. Import the Workflow

1. Copy the contents of `pharmacy-inventory-workflow.json`
2. In n8n, go to **Workflows** → **Import from JSON**
3. Paste the JSON content and import

### 2. Configure Credentials

You'll need to set up the following credentials in n8n:

#### Smart Glasses API
```
Credential Type: HTTP Header Auth
Name: smartGlassesApi
Headers:
  - Authorization: Bearer YOUR_SMART_GLASSES_API_TOKEN
```

#### ERP System API
```
Credential Type: HTTP Header Auth  
Name: erpSystem
Headers:
  - Authorization: Bearer YOUR_ERP_API_TOKEN
```

#### Audit System API
```
Credential Type: HTTP Header Auth
Name: auditSystem  
Headers:
  - Authorization: Bearer YOUR_AUDIT_API_TOKEN
```

#### Email Configuration
```
Credential Type: SMTP
Configure your SMTP settings for email reports
```

#### Slack Integration
```
Credential Type: Slack OAuth2
Set up Slack app with appropriate permissions
```

### 3. Update API Endpoints

Replace the following placeholder URLs in the workflow:

- `https://smart-glasses-api.example.com` → Your smart glasses API endpoint
- `https://api.your-erp-system.com` → Your ERP system API
- `https://api.your-audit-system.com` → Your audit system API

### 4. Configure Webhook

After importing, note the webhook URL from the "Inventory Scan Webhook" node. Configure your scanning devices to send POST requests to this endpoint.

## API Specifications

### Webhook Input Format

Send POST requests to the webhook with this JSON structure:

```json
{
  "productId": "string",          // Required: Unique product identifier
  "quantity": "number",           // Required: Scanned quantity
  "rawExpiryDate": "string",      // Required: Raw expiry date text
  "imageUrl": "string",           // Optional: Product image URL
  "deviceId": "string",           // Optional: Scanning device identifier
  "scanTimestamp": "string"       // Optional: Scan timestamp (ISO format)
}
```

### Smart Glasses API Integration

The workflow expects your smart glasses API to support these endpoints:

#### Individual Device Alert
```
POST /alert/{deviceId}
Authorization: Bearer {token}
Content-Type: application/json

{
  "alertType": "manual_review_required|expired_product|near_expiry",
  "message": "Alert message text",
  "productId": "product-123",
  "soundAlert": true,
  "vibrationPattern": "short-long-short|urgent|gentle",
  "displayDuration": 10000,
  "backgroundColor": "#FF0000"
}
```

#### Broadcast Alert (All Devices)
```
POST /broadcast
Authorization: Bearer {token}
Content-Type: application/json

{
  "alertType": "expired_product",
  "message": "CRITICAL: Product expired",
  "soundAlert": true,
  "vibrationPattern": "urgent",
  "displayDuration": 15000
}
```

## Workflow Logic Flow

### Main Processing Flow

1. **Webhook Trigger** → Receives scan data
2. **Input Validation** → Validates required fields
3. **Expiry Date Parsing** → Processes raw date text
4. **Status Routing** → Routes based on product status:
   - Unparseable expiry → Manual review alert
   - Expired product → Critical alert
   - Near expiry → Warning alert
   - Valid product → Continue processing
5. **Database Update** → Updates ERP/inventory system
6. **Stock Level Check** → Evaluates reorder needs
7. **Audit Logging** → Creates audit trail
8. **Response** → Returns success/failure to device

### Reporting Flow

1. **Cron Trigger** → Weekly schedule (Mondays at 8 AM)
2. **Data Fetch** → Retrieves inventory summary
3. **Report Generation** → Creates HTML report
4. **Email Delivery** → Sends to inventory managers

## Configuration Options

### Date Format Support

The workflow supports these date formats out of the box:

- `MM/DD/YYYY`, `MM-DD-YYYY`, `MM.DD.YYYY`
- `DD/MM/YYYY`, `DD-MM-YYYY`, `DD.MM.YYYY`  
- `YYYY/MM/DD`, `YYYY-MM-DD`
- `MM/YY`, `MM-YY`
- `EXP MM/YY`, `BEST BY MM/YY`
- ISO formats with time

### Stock Level Thresholds

Customize reorder thresholds in the "Check Stock Levels" node:

```javascript
const reorderThresholds = {
  'default': 10,
  'medication': 5,
  'controlled': 3,
  'supplies': 20
};
```

### Alert Timing

Modify expiry alert windows in the "Parse Expiry Date" node:

```javascript
// Current: 30 days for near expiry
if (daysUntilExpiry <= 30) {
  productStatus = 'near_expiry';
}

// Example: Change to 45 days
if (daysUntilExpiry <= 45) {
  productStatus = 'near_expiry';
}
```

## Robustness & Scalability Recommendations

### 1. Error Handling & Resilience

- **Retry Logic**: Add retry nodes for API calls with exponential backoff
- **Fallback Mechanisms**: Implement fallback notification methods (SMS if email fails)
- **Circuit Breakers**: Add timeout and circuit breaker patterns for external APIs
- **Data Validation**: Enhance input validation with additional business rules

### 2. Performance Optimization

- **Batch Processing**: For high-volume scenarios, implement batch processing for database updates
- **Caching**: Cache frequently accessed data (product info, thresholds)
- **Async Processing**: Use message queues for non-critical operations
- **Database Optimization**: Index key fields in your inventory database

### 3. Scalability Considerations

- **Horizontal Scaling**: Deploy multiple n8n instances with load balancing
- **Database Scaling**: Use read replicas for reporting queries
- **API Rate Limiting**: Implement rate limiting and quota management
- **Monitoring**: Add comprehensive monitoring and alerting

### 4. Security Best Practices

- **API Security**: Use API keys, OAuth 2.0, or JWT tokens
- **Data Encryption**: Encrypt sensitive data in transit and at rest
- **Access Control**: Implement role-based access control
- **Audit Compliance**: Ensure audit logs meet regulatory requirements

### 5. Monitoring & Observability

Add these monitoring capabilities:

```javascript
// Example monitoring node
const metrics = {
  processingTime: Date.now() - startTime,
  success: true,
  alertLevel: $json.alertLevel,
  deviceId: $json.deviceId
};

// Send to monitoring service
await sendMetrics(metrics);
```

### 6. Business Continuity

- **Backup Strategies**: Regular backups of workflow and data
- **Disaster Recovery**: Document recovery procedures
- **Offline Capabilities**: Design for partial offline operation
- **Data Synchronization**: Handle data sync when systems come back online

## Testing & Validation

### Test Scenarios

1. **Valid Scan Data**: Test with properly formatted data
2. **Invalid Expiry Dates**: Test unparseable date scenarios
3. **Expired Products**: Test immediate alert triggers
4. **Low Stock**: Test reorder alert functionality
5. **Device Communication**: Test smart glasses integration
6. **Report Generation**: Validate weekly report accuracy

### Sample Test Data

```json
{
  "productId": "MED-001",
  "quantity": 5,
  "rawExpiryDate": "EXP 12/24",
  "deviceId": "glasses-001",
  "scanTimestamp": "2024-01-15T10:30:00Z"
}
```

## Troubleshooting

### Common Issues

1. **Date Parsing Failures**: Check date format patterns in the parsing code
2. **API Connection Issues**: Verify credentials and endpoint URLs
3. **Missing Alerts**: Check smart glasses API connectivity
4. **Report Not Sent**: Verify email/Slack configurations

### Debug Mode

Enable debug mode by adding console.log statements in JavaScript nodes and checking execution logs.

## Support & Maintenance

### Regular Maintenance Tasks

- Monitor workflow execution logs
- Update API credentials as needed
- Review and adjust alert thresholds
- Validate report accuracy
- Test smart glasses integration
- Update date parsing patterns as needed

### Performance Monitoring

Monitor these metrics:
- Workflow execution time
- API response times
- Alert delivery success rates
- Date parsing success rates
- Database update performance

## Compliance & Regulatory Considerations

- **FDA Compliance**: Ensure audit trails meet FDA requirements
- **HIPAA**: Protect patient data if applicable
- **Data Retention**: Implement appropriate data retention policies
- **Validation**: Document system validation for regulatory audits

This workflow provides a robust foundation for pharmacy inventory management with room for customization based on specific requirements and regulatory needs. 