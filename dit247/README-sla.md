# SLA Definition
## Objective
Ensure that the image resizing flow operates efficiently, with a clear performance benchmark that guarantees timely processing of images.

## Service Description

- **Service:** Image Resizing Flow
- **Scope:** The service covers the entire process from the moment an image is uploaded to the MinIO bucket **dit247** until the resized image is uploaded to the MinIO bucket (**dit247c**) and a triggered webhook request is received to acknowledge completion.

## Performance Metrics
### Response Time
- **Definition:** The time taken from the initial upload of an image to **dit247** until the resized image is uploaded to **dit247c** and the webhook triggers.
- **Guaranteed Performance:** The service guarantees that **99%** of image resizing operations will be completed within **10 seconds**.
- **Measurement Method:** The start and end times are recorded for each image, and the durations are monitored via a Node-RED chart node. A Continuous Distribution Function (CDF) is used to analyze these durations and ensure compliance.
### Availability
- **Service Uptime:** The system is expected to be operational and available **24/7** with an uptime of **99.9%**.
- **Downtime Impact:** If the service experiences downtime that affects more than **0.1%** of operations in a given month, compensatory measures or adjustments will be provided.
### Penalties:
- **Non-Compliance:** If the SLA is breached, meaning the processing time exceeds the **10-second** threshold for more than **1%** of the images, or if uptime falls below **99.9%**, the service provider may be required to investigate the cause and propose optimizations to ensure future compliance.

# SLA Monitoring and Reporting
- **Monitoring Tools:** Node-RED will monitor and log the duration of each image processing flow, with alerts configured to notify administrators if processing times exceed the SLA limits.
- **Reporting Frequency:** SLA performance will be reviewed monthly, with reports generated to assess compliance and identify any areas requiring improvement.

This SLA ensures that your cloud-based image resizing service is reliable, with clear performance expectations and monitoring mechanisms to maintain high standards.