# CompressionMiddleware

GZip compression for HTTP responses to reduce bandwidth and improve load times.

## Installation

```python
from src import CompressionMiddleware, CompressionConfig
```

## Quick Start

```python
from fastapi import FastAPI
from src import CompressionMiddleware

app = FastAPI()

app.add_middleware(CompressionMiddleware)
```

## Configuration

### CompressionConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `minimum_size` | `int` | `500` | Minimum bytes to compress |
| `compression_level` | `int` | `6` | GZip level (1-9) |
| `compressible_types` | `tuple` | JSON, HTML, etc. | MIME types to compress |

### Compression Levels

| Level | Speed | Compression |
|-------|-------|-------------|
| 1 | Fastest | Lowest |
| 6 | Balanced | Good (default) |
| 9 | Slowest | Best |

## Response Headers

When compressed:
```http
Content-Encoding: gzip
Vary: Accept-Encoding
```

## Examples

### Default Configuration

```python
app.add_middleware(CompressionMiddleware)
```

### High Compression

```python
from src import CompressionMiddleware, CompressionConfig

config = CompressionConfig(
    compression_level=9,  # Maximum compression
)

app.add_middleware(CompressionMiddleware, config=config)
```

### Custom Threshold

```python
config = CompressionConfig(
    minimum_size=1000,  # Only compress responses > 1KB
)
```

### Fast Compression

```python
config = CompressionConfig(
    compression_level=1,  # Fastest compression
)
```

### Custom Content Types

```python
config = CompressionConfig(
    compressible_types=(
        "application/json",
        "text/html",
        "text/css",
        "application/javascript",
        "text/xml",
        "application/xml",
        "image/svg+xml",
    ),
)
```

### Exclude Paths

```python
app.add_middleware(
    CompressionMiddleware,
    exclude_paths={"/images", "/videos"},
)
```

## Content Types

Default compressible types:
- `text/html`
- `text/css`
- `text/plain`
- `text/xml`
- `text/javascript`
- `application/json`
- `application/javascript`
- `application/xml`
- `application/xhtml+xml`
- `image/svg+xml`

**Not compressed by default:**
- Binary files (images, videos)
- Already compressed formats (gzip, zip)
- Very small responses

## Client Requirements

The client must accept gzip encoding:

```http
GET /api/data HTTP/1.1
Accept-Encoding: gzip, deflate
```

If `Accept-Encoding` doesn't include `gzip`, responses are not compressed.

## How It Works

1. Check if client accepts gzip (`Accept-Encoding` header)
2. Generate response normally
3. Check if response meets criteria:
   - Size >= minimum_size
   - Content-Type is compressible
   - Not already compressed
4. Compress response body
5. Add `Content-Encoding: gzip` header
6. Add `Vary: Accept-Encoding` header

## Performance Considerations

### CPU vs Bandwidth Trade-off

| Scenario | Recommendation |
|----------|----------------|
| High bandwidth costs | Use level 9 |
| CPU-constrained | Use level 1-3 |
| Balanced | Use level 6 (default) |

### When NOT to Compress

- Very small responses (< 500 bytes)
- Already compressed content (gzip, images)
- Streaming responses
- WebSocket connections

## Middleware Order

Place `CompressionMiddleware` first (outermost) to compress final responses:

```python
# First added = compresses everything
app.add_middleware(CompressionMiddleware)

# Other middleware
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
```

## Streaming Responses

Streaming responses are passed through without compression:

```python
from starlette.responses import StreamingResponse

@app.get("/stream")
async def stream():
    async def generate():
        for i in range(100):
            yield f"data: {i}\n"
    
    return StreamingResponse(generate(), media_type="text/plain")
```

## Testing Compression

```bash
# Request with gzip
curl -H "Accept-Encoding: gzip" https://api.example.com/data -o response.gz

# Check if gzipped
file response.gz
# Output: response.gz: gzip compressed data

# Decompress
gunzip response.gz
cat response
```

## Measuring Compression Ratio

```python
import gzip

original_size = len(response_body)
compressed_size = len(gzip.compress(response_body))
ratio = compressed_size / original_size

print(f"Compression ratio: {ratio:.2%}")
print(f"Saved: {100 - ratio * 100:.1f}%")
```

Typical compression ratios:
- JSON: 70-90% reduction
- HTML: 70-85% reduction
- Plain text: 60-80% reduction

## Best Practices

1. **Use default settings** - Level 6 is balanced
2. **Set appropriate minimum size** - Don't compress tiny responses
3. **Exclude binary content** - Already compressed or not compressible
4. **Add Vary header** - For correct caching
5. **Test compression** - Verify savings are worthwhile

## Related

- [CacheMiddleware](cache.md) - HTTP caching
- [TimingMiddleware](timing.md) - Response timing

