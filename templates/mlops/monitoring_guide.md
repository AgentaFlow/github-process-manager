# MLOps Monitoring and Observability Guide

## Introduction

This guide covers comprehensive monitoring strategies for machine learning models in production, including performance tracking, data drift detection, and operational metrics.

---

## 1. Model Performance Monitoring

### Key Performance Indicators (KPIs)

#### Prediction Accuracy Metrics
Monitor these metrics continuously in production:

**Classification Models:**
- **Accuracy**: Overall prediction correctness
  - Alert if accuracy drops > 5% from baseline
- **Precision**: True positives / (True positives + False positives)
  - Critical for spam detection, fraud detection
- **Recall**: True positives / (True positives + False negatives)
  - Critical for disease detection, security threats
- **F1-Score**: Harmonic mean of precision and recall
- **AUC-ROC**: Area under ROC curve
  - Threshold: Alert if AUC < 0.75

**Regression Models:**
- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes large errors
- **R² Score**: Variance explained by model
- **MAPE (Mean Absolute Percentage Error)**: Percentage-based error

#### Performance Benchmarks
Set baselines and alert thresholds:

```
Metric          | Baseline | Warning Threshold | Critical Threshold
----------------|----------|-------------------|-------------------
Accuracy        | 94.5%    | < 92%            | < 90%
Precision       | 91.2%    | < 88%            | < 85%
Recall          | 93.8%    | < 90%            | < 87%
F1-Score        | 0.925    | < 0.90           | < 0.87
Latency P95     | 85ms     | > 150ms          | > 250ms
Error Rate      | 0.5%     | > 2%             | > 5%
```

### Prediction Distribution Monitoring

Track prediction output distribution over time:

- **Class Distribution** (Classification):
  - Monitor percentage of predictions per class
  - Alert if distribution shifts significantly
  - Example: If fraud predictions jump from 2% to 15%, investigate

- **Value Distribution** (Regression):
  - Monitor mean, median, standard deviation
  - Track min/max prediction values
  - Alert on significant distribution changes

### Confidence Score Analysis

For models that output confidence scores:

- **Average Confidence**: Track mean confidence over time
- **Low Confidence Predictions**: Monitor percentage with confidence < threshold
- **Calibration**: Verify predicted probabilities match actual outcomes
  - Well-calibrated: If model predicts 80% confidence, it should be correct 80% of time

---

## 2. Latency and Throughput Monitoring

### Latency Metrics

Track inference latency at multiple percentiles:

```
P50 (Median):  50th percentile - typical request
P75:           75th percentile
P95:           95th percentile - slower requests
P99:           99th percentile - outliers
P99.9:         99.9th percentile - worst case
```

**Example Latency SLA:**
- P50 < 50ms
- P95 < 100ms
- P99 < 200ms
- P99.9 < 500ms

**Latency Breakdown:**
- Preprocessing time
- Model inference time
- Postprocessing time
- Network time
- Queue wait time

### Throughput Metrics

- **Requests Per Second (RPS)**: Total requests handled
- **Successful Requests**: Requests completed successfully
- **Failed Requests**: Requests that returned errors
- **Concurrent Requests**: Number of simultaneous requests

**Alert Conditions:**
- Throughput drops below expected baseline
- Queue depth exceeds threshold (backlog building up)
- Request timeout rate > 1%

---

## 3. Data Drift Detection

### Input Data Drift

Monitor changes in input feature distributions over time.

#### Statistical Tests

**Kolmogorov-Smirnov (K-S) Test:**
- Compares two distributions
- Null hypothesis: Distributions are the same
- Alert if p-value < 0.05

**Chi-Squared Test:**
- For categorical features
- Tests if distribution has changed
- Alert if p-value < 0.05

**Population Stability Index (PSI):**
```
PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)

Interpretation:
PSI < 0.1:  No significant change
PSI 0.1-0.2: Small change, monitor closely
PSI > 0.2:  Significant drift, retraining recommended
```

#### Feature Monitoring

For each feature, track:
- **Mean and Standard Deviation**: Detect shifts in distribution center
- **Min/Max Values**: Detect range changes
- **Missing Value Rate**: Detect data quality issues
- **Cardinality**: For categorical features, track unique value count

**Example Alert Rules:**
```
Feature: age
- Alert if mean shifts > 2 standard deviations
- Alert if missing rate > 5%
- Alert if min/max outside expected range

Feature: country (categorical)
- Alert if new countries appear
- Alert if distribution changes (PSI > 0.2)
```

### Prediction Drift

Monitor changes in model output distribution:

- **Class Distribution Drift** (Classification):
  - Track percentage in each class over time
  - Alert if distribution changes significantly

- **Output Value Drift** (Regression):
  - Monitor mean, median, variance of predictions
  - Alert on significant changes

**Drift Alert Example:**
```
Historical: 98% Class 0, 2% Class 1
Current:    85% Class 0, 15% Class 1

→ Significant drift detected, investigate cause
```

### Concept Drift

The relationship between features and target changes:

- **Gradual Drift**: Slow change over time (seasonal patterns)
- **Sudden Drift**: Abrupt change (policy change, market shift)
- **Recurring Drift**: Cyclic patterns (day/night, weekday/weekend)

**Detection Strategy:**
- Compare recent model performance to historical baseline
- Use sliding window to track performance over time
- Alert if accuracy degrades consistently

---

## 4. Data Quality Monitoring

### Input Validation

**Schema Validation:**
- [ ] All required fields present
- [ ] Data types correct (int, float, string)
- [ ] Field lengths within limits
- [ ] No unexpected null values

**Range Validation:**
- [ ] Numerical values within expected range
- [ ] Categorical values from known set
- [ ] Date values within reasonable range
- [ ] String formats match patterns (email, phone)

**Logical Validation:**
- [ ] Business rules satisfied (age > 0, price > 0)
- [ ] Referential integrity maintained
- [ ] Temporal consistency (start_date < end_date)

### Data Quality Metrics

Track over time:
- **Completeness**: % of required fields populated
- **Accuracy**: % of values that are correct
- **Consistency**: % of records without conflicts
- **Timeliness**: Age of data (freshness)
- **Validity**: % of values matching expected format

**Data Quality Dashboard:**
```
Metric          | Target | Current | Status
----------------|--------|---------|-------
Completeness    | > 99%  | 99.8%   | ✓
Accuracy        | > 95%  | 97.2%   | ✓
Consistency     | > 98%  | 96.5%   | ⚠
Timeliness      | < 1hr  | 45min   | ✓
Validity        | > 99%  | 98.8%   | ⚠
```

---

## 5. Infrastructure and Resource Monitoring

### System Metrics

**CPU Usage:**
- Monitor CPU utilization per container/instance
- Alert if sustained usage > 80%
- Track CPU throttling events

**Memory Usage:**
- Monitor RAM utilization
- Alert if usage > 85%
- Track out-of-memory (OOM) errors

**GPU Usage (if applicable):**
- GPU utilization percentage
- GPU memory usage
- Temperature monitoring

**Disk I/O:**
- Read/write throughput
- Disk space utilization
- I/O wait time

**Network:**
- Network bandwidth usage
- Packet loss rate
- Connection errors

### Container/Pod Metrics (Kubernetes)

- **Pod Count**: Number of running pods
- **Pod Restarts**: Frequent restarts indicate issues
- **Pod Status**: Running, pending, failed, unknown
- **Resource Limits**: CPU/memory requests vs limits
- **Node Health**: Status of underlying nodes

---

## 6. Error Monitoring and Logging

### Error Classification

**Client Errors (4xx):**
- 400 Bad Request: Invalid input data
- 401 Unauthorized: Authentication failed
- 403 Forbidden: Authorization failed
- 404 Not Found: Endpoint doesn't exist
- 429 Too Many Requests: Rate limit exceeded

**Server Errors (5xx):**
- 500 Internal Server Error: Unhandled exception
- 502 Bad Gateway: Upstream service failure
- 503 Service Unavailable: Service overloaded
- 504 Gateway Timeout: Upstream timeout

**Application Errors:**
- Model loading failures
- Preprocessing errors
- Invalid predictions (NaN, Infinity)
- Database connection errors
- Cache errors

### Error Rate Monitoring

```
Total Requests:     10,000
Successful (2xx):    9,850 (98.5%)
Client Errors (4xx):   100 (1.0%)
Server Errors (5xx):    50 (0.5%)

Error Rate: 1.5%
```

**Alert Thresholds:**
- Warning: Error rate > 1%
- Critical: Error rate > 5%
- Emergency: Error rate > 10%

### Logging Best Practices

**Structured Logging (JSON):**
```json
{
  "timestamp": "2026-02-09T10:15:30Z",
  "level": "INFO",
  "model": "fraud-detector",
  "version": "2.1.0",
  "request_id": "abc123",
  "latency_ms": 87,
  "prediction": 0,
  "confidence": 0.92,
  "input_hash": "d41d8cd98f00b204e9800998ecf8427e"
}
```

**Log Levels:**
- **DEBUG**: Detailed diagnostic information
- **INFO**: General informational messages
- **WARNING**: Warning messages (degraded performance)
- **ERROR**: Error messages (failed requests)
- **CRITICAL**: Critical issues (service down)

**What to Log:**
- Every prediction (or sampled percentage)
- Request/response metadata
- Latency for each stage
- Errors and exceptions
- Model version used
- Input feature hashes (for privacy)

---

## 7. Alert Configuration

### Alert Levels

**P0 - Critical (Immediate Response):**
- Model service down (health check failing)
- Error rate > 10%
- Data pipeline broken
- Security breach detected

**P1 - High (15 min response):**
- Error rate > 5%
- Latency P95 > 2x baseline
- Accuracy drop > 10%
- Memory/CPU > 90%

**P2 - Medium (1 hour response):**
- Error rate > 2%
- Latency P95 > 1.5x baseline
- Accuracy drop > 5%
- Data drift detected (PSI > 0.2)

**P3 - Low (24 hour response):**
- Error rate > 1%
- Warning level resource usage
- Data quality issues
- Non-critical performance degradation

### Alert Rules Examples

```yaml
# Example alert configuration

- alert: HighErrorRate
  expr: error_rate > 0.05
  for: 5m
  severity: P1
  annotations:
    summary: "Error rate above 5% for 5 minutes"
    
- alert: ModelAccuracyDrop
  expr: accuracy < 0.90
  for: 15m
  severity: P2
  annotations:
    summary: "Model accuracy dropped below 90%"
    
- alert: HighLatency
  expr: latency_p95 > 200
  for: 10m
  severity: P1
  annotations:
    summary: "P95 latency above 200ms for 10 minutes"
```

### On-Call Rotation

- Define on-call rotation schedule
- Ensure 24/7 coverage for P0/P1 alerts
- Document escalation procedures
- Provide runbooks for common issues

---

## 8. Dashboards and Visualization

### Real-Time Operations Dashboard

**Key Metrics (Last 1 Hour):**
- Request volume (RPS)
- Success rate
- Error rate by type
- Latency percentiles (P50, P95, P99)
- Active instances/pods

### Model Performance Dashboard

**Key Metrics (Last 24 Hours):**
- Prediction accuracy
- Precision/Recall/F1
- Confusion matrix heatmap
- Confidence score distribution
- Prediction class distribution

### Data Quality Dashboard

**Key Metrics (Last 7 Days):**
- Feature distributions
- Missing value rates
- Data drift scores (PSI)
- Schema validation failures
- Data freshness

### Infrastructure Dashboard

**Key Metrics:**
- CPU utilization by instance
- Memory utilization by instance
- Network throughput
- Disk I/O
- Auto-scaling events

---

## 9. Model Retraining Triggers

### Automatic Retraining Conditions

**Performance-Based:**
- Accuracy drops below 92% for 3 consecutive days
- F1-score decreases by more than 5% from baseline
- Error rate exceeds 3% for 1 week

**Drift-Based:**
- Data drift (PSI > 0.25) detected for 5+ key features
- Prediction drift significant for 7+ consecutive days
- Concept drift indicated by declining performance

**Time-Based:**
- Scheduled monthly retraining
- Quarterly model refresh
- After major product changes

**Data-Based:**
- New labeled data threshold reached (e.g., 10,000 samples)
- Data quality improved significantly
- New feature data available

### Retraining Workflow

1. **Trigger Detection**: Automated or manual trigger
2. **Data Collection**: Gather recent production data
3. **Data Validation**: Ensure quality and completeness
4. **Model Training**: Train candidate model
5. **Validation**: Offline validation against hold-out set
6. **A/B Testing**: Online validation with small traffic
7. **Gradual Rollout**: Canary → 50% → 100% traffic
8. **Monitoring**: Enhanced monitoring post-deployment

---

## 10. Incident Response

### Incident Severity Classification

**SEV-0 (Critical):**
- Complete service outage
- Data breach or security incident
- Widespread incorrect predictions

**SEV-1 (High):**
- Significant performance degradation
- Partial service outage
- High error rates affecting users

**SEV-2 (Medium):**
- Isolated performance issues
- Non-critical feature failures
- Data quality problems

**SEV-3 (Low):**
- Minor issues
- Performance optimization needed
- Documentation updates

### Incident Response Procedure

1. **Detection**: Alert fires or issue reported
2. **Acknowledgment**: On-call engineer acknowledges (< 5 min)
3. **Assessment**: Determine severity and impact
4. **Escalation**: Involve additional team members if needed
5. **Mitigation**: Immediate fix or rollback
6. **Communication**: Update stakeholders
7. **Resolution**: Permanent fix deployed
8. **Post-Mortem**: Document lessons learned

### Runbook Example: High Error Rate

**Symptom**: Error rate > 5% for 10 minutes

**Investigation Steps:**
1. Check recent deployments (possible bad release)
2. Review error logs for common patterns
3. Check upstream service status
4. Verify infrastructure health (CPU, memory, disk)
5. Check data quality (schema changes, missing fields)

**Mitigation:**
- If recent deployment: Rollback to previous version
- If infrastructure issue: Scale up resources
- If upstream failure: Enable circuit breaker
- If data issue: Enable input validation fallback

**Post-Incident:**
- Create post-mortem document
- Update runbook based on learnings
- Schedule follow-up improvements

---

## 11. Tools and Technologies

### Monitoring Platforms
- **Prometheus + Grafana**: Metrics and dashboards
- **Datadog**: Unified monitoring platform
- **New Relic**: APM and infrastructure monitoring
- **Splunk**: Log aggregation and analysis
- **CloudWatch**: AWS native monitoring

### Model Monitoring Tools
- **Evidently AI**: ML monitoring and drift detection
- **Fiddler**: ML monitoring and explainability
- **Arize**: Model performance management
- **WhyLabs**: Data and ML monitoring
- **Neptune.ai**: Experiment tracking and monitoring

### Alerting
- **PagerDuty**: Incident management and on-call
- **Opsgenie**: Alert management and escalation
- **VictorOps**: Incident response platform

### Logging
- **ELK Stack**: Elasticsearch, Logstash, Kibana
- **Loki**: Log aggregation by Grafana
- **CloudWatch Logs**: AWS logging service

---

## 12. Best Practices Summary

✅ **Do:**
- Monitor both model performance AND infrastructure
- Set up comprehensive alerting with appropriate thresholds
- Implement automated drift detection
- Log predictions for audit trail and retraining
- Create dashboards for different audiences (ops, data science, business)
- Document incident response procedures
- Regularly review and update monitoring strategies
- Practice incident response (fire drills)

❌ **Don't:**
- Rely solely on accuracy metrics
- Ignore data drift
- Set alert thresholds too sensitive (alert fatigue)
- Forget to monitor data quality
- Log sensitive PII without anonymization
- Deploy without monitoring dashboards
- Skip post-incident reviews

---

## Conclusion

Effective monitoring is essential for production ML systems. Start with basic metrics and alerting, then gradually add sophistication as you learn your model's behavior patterns. Remember: you can't improve what you don't measure.
