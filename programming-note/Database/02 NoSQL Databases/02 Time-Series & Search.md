---
tags:
- database
- nosql
- programming
- sql
---

# 02 Time-Series & Search Databases

Specialized databases for specialized problems: time-series for metrics/IoT, full-text search for... search.

---

## Time-Series — InfluxDB & TimescaleDB

Optimized for data points with timestamps: metrics, sensor readings, stock prices, logs.

### The Time-Series Pattern

```
timestamp          | device_id | temperature | humidity
2024-01-15 14:00:00 | sensor_1  | 22.5        | 65.0
2024-01-15 14:01:00 | sensor_1  | 22.6        | 64.8
2024-01-15 14:02:00 | sensor_1  | 22.7        | 64.9
```

| Characteristic | Time-Series DB | Regular RDBMS |
|---------------|:---:|:---:|
| **Write pattern** | Append-only. Almost no updates/deletes. | Mixed. |
| **Read pattern** | Time-range queries. Aggregations over windows. | Any query. |
| **Compression** | Specialized (delta-of-delta, run-length) | Generic. |
| **Retention** | Auto-drop old data (downsampling) | Manual purging. |

### InfluxDB — Purpose-Built Time-Series

```
Measurement: temperature
Tags: device_id=sensor_1, location=room_a
Fields: value=22.5, humidity=65.0
Timestamp: 2024-01-15T14:00:00Z
```

### TimescaleDB — PostgreSQL Extension

Best of both worlds: PostgreSQL + time-series optimization (hypertables, automatic partitioning).

```sql
-- Create a hypertable — automatically partitions by time
CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    device_id TEXT NOT NULL,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);
SELECT create_hypertable('sensor_data', 'time');

-- Time-based query — hypertable automatically excludes irrelevant chunks
SELECT time_bucket('1 hour', time) AS hour,
       device_id,
       AVG(temperature)
FROM sensor_data
WHERE time > NOW() - INTERVAL '7 days'
GROUP BY hour, device_id;
```

---

## Full-Text Search — Elasticsearch

Built on Apache Lucene. Turns unstructured text into searchable, analyzable data.

### Core Concepts

| Concept | What It Is |
|---------|-----------|
| **Index** | Like a database. Holds documents. |
| **Document** | Like a row. JSON object. |
| **Mapping** | Like a schema. Defines field types and analyzers. |
| **Inverted Index** | Maps every word → documents that contain it. |
| **Analyzer** | Tokenizes and normalizes text for indexing and searching. |

### The Inverted Index

```
Document 1: "The quick brown fox"
Document 2: "The lazy brown dog"

Inverted Index:
"the"   → [1, 2]
"quick" → [1]
"brown" → [1, 2]
"fox"   → [1]
"lazy"  → [2]
"dog"   → [2]
```

### Query DSL

```json
// Search products with fuzzy matching, filters, and aggregations
{
  "query": {
    "bool": {
      "must": [
        { "match": { "name": { "query": "wireless headfones", "fuzziness": 1 } } }
      ],
      "filter": [
        { "range": { "price": { "lte": 100 } } },
        { "term": { "in_stock": true } }
      ]
    }
  },
  "aggs": {
    "by_category": {
      "terms": { "field": "category.keyword" }
    }
  }
}
```

### When to Use Elasticsearch

| ✅ Good Fit | ❌ Bad Fit |
|-----------|-----------|
| Full-text product search | Primary database (it's a search engine, not a DB) |
| Log aggregation (ELK stack) | Transactions |
| Autocomplete/typeahead | Relational queries |
| Analytics on semi-structured data | Frequent updates (Lucene segments are immutable) |

---

## Sources

- InfluxDB Docs — https://docs.influxdata.com/
- TimescaleDB Docs — https://docs.timescale.com/
- Elasticsearch Guide — https://www.elastic.co/guide/en/elasticsearch/reference/current/
