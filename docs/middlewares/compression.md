# CompressionMiddleware

GZip compression for HTTP responses, reducing bandwidth and improving load times.

## Installation

```python
from fastmiddleware import CompressionMiddleware, CompressionConfig

```

## Quick Start

```python
from fastapi import FastAPI
from fastmiddleware import CompressionMiddleware

app = FastAPI()

app.add_middleware(CompressionMiddleware)

```

## Configuration

### CompressionConfig

|Parameter|Type|Default|Description|
| ----------- | ------ | --------- | ------------- |
|`minimum_size`|`int`|`500`|Minimum bytes to compress|
|`compression_level`|`int`|`6`|GZip level (1-9)|
|`compressible_types`|`tuple`|See below|MIME types to compress|

### Default Compressible Types

```python
compressible_types = (
    "text/html",
    "text/css",
    "text/plain",
    "text/xml",
    "text/javascript",
    "application/json",
    "application/javascript",
    "application/xml",
    "application/xhtml+xml",
    "image/svg+xml",
)

```

## Response Headers

When compression is applied:

```http
Content-Encoding: gzip
Vary: Accept-Encoding

```

## Examples

### Default Configuration

```python
app.add_middleware(CompressionMiddleware)

# Compresses responses > 500 bytes

# Uses compression level 6

```

### Custom Minimum Size

```python
app.add_middleware(
    CompressionMiddleware,
    minimum_size=1000,  # Only compress responses > 1KB
)

```

### Maximum Compression

```python
app.add_middleware(
    CompressionMiddleware,
    compression_level=9,  # Best compression, more CPU
)

```

### Fast Compression

```python
app.add_middleware(
    CompressionMiddleware,
    compression_level=1,  # Fastest, less compression
)

```

### Custom Compressible Types

```python
from fastmiddleware import CompressionConfig

config = CompressionConfig(
    compressible_types=(
        "application/json",
        "text/html",
        "text/css",
        "application/javascript",
        "application/wasm",  # Add WebAssembly
    ),
)

app.add_middleware(CompressionMiddleware, config=config)

```

### Full Configuration

```python
from fastmiddleware import CompressionMiddleware, CompressionConfig

config = CompressionConfig(
    minimum_size=1000,
    compression_level=6,
    compressible_types=(
        "application/json",
        "text/html",
        "text/css",
        "application/javascript",
    ),
)

app.add_middleware(CompressionMiddleware, config=config)

```

## Compression Levels

|Level|Speed|Ratio|Use Case|
| ------- | ------- | ------- | ---------- |
|1|Fastest|~50%|High-traffic, CPU-limited|
|4-5|Balanced|~65%|General use|
|6|Default|~70%|Good balance|
|9|Slowest|~75%|Bandwidth-critical|

## What Gets Compressed

✅ Compressed:

- JSON responses

- HTML pages

- CSS files

- JavaScript

- SVG images

- XML data

❌ Not Compressed:

- Images (JPEG, PNG, GIF, WebP)

- Videos

- Already compressed files (zip, gzip)

- Small responses (< minimum_size)

- Streaming responses

## Path Exclusion

Exclude paths from compression:

```python
app.add_middleware(
    CompressionMiddleware,
    exclude_paths={"/stream", "/sse"},
)

```

## Client Requirements

Clients must include `Accept-Encoding` header:

```http
Accept-Encoding: gzip, deflate

```

Most browsers and HTTP clients do this automatically.

## Middleware Order

Place CompressionMiddleware early (executed late):

```python

# Add first = executed last = compresses final response
app.add_middleware(CompressionMiddleware)  # Add first
app.add_middleware(TimingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware)  # Add last

```

## Performance Considerations

### CPU vs Bandwidth Trade-off

|Scenario|Recommendation|
| ---------- | ---------------- |
|High bandwidth cost|Level 9|
|High CPU cost|Level 1-3|
|Balanced|Level 5-6|

### When to Skip Compression

- Pre-compressed static files (use CDN)
- Small responses (overhead > savings)
- Real-time streaming
- Binary files (images, videos)

## Caching Considerations

The `Vary: Accept-Encoding` header ensures caches store separate versions:

```http
Vary: Accept-Encoding

```

This prevents serving compressed content to clients that don't support it.

## Static File Compression

For static files, consider pre-compression:

```python

# In production, serve pre-compressed files

# Don't compress on every request

# Use nginx/CDN with:
gzip_static on;

```

## Best Practices

1. **Set appropriate minimum size** - Don't compress tiny responses
2. **Exclude binary content** - Already compressed
3. **Pre-compress static files** - In production
4. **Monitor CPU usage** - Adjust level if needed
5. **Use CDN compression** - Offload to edge

## Related Middlewares

- [CacheMiddleware](./cache.md) - Cache compressed responses
- [TimingMiddleware](./timing.md) - Measure compression overhead
