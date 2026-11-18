"""Extract the evaluation database using HTTP ranges from the Zenodo ZIP."""
import concurrent.futures
import pathlib
import struct
import urllib.request
import zlib

URL = 'https://zenodo.org/api/records/10033132/files/PASDA.zip/content'
OFFSET = 18747369
COMPRESSED_SIZE = 5452169945
ROOT = pathlib.Path(__file__).resolve().parent


def fetch(start, end):
    request = urllib.request.Request(URL, headers={'Range': f'bytes={start}-{end}'})
    with urllib.request.urlopen(request, timeout=300) as response:
        if response.status != 206:
            raise RuntimeError(f'Expected HTTP 206, got {response.status}')
        data = response.read()
    if len(data) != end - start + 1:
        raise RuntimeError(f'Incomplete range {start}-{end}: {len(data)} bytes')
    return data


header = fetch(OFFSET, OFFSET + 29)
fields = struct.unpack('<4s5H3I2H', header)
start = OFFSET + 30 + fields[-2] + fields[-1]
chunk_size = 32 * 1024 * 1024
chunks = [(position, min(chunk_size, COMPRESSED_SIZE - position))
          for position in range(0, COMPRESSED_SIZE, chunk_size)]
compressed_path = ROOT / 'results.db.deflate'
with compressed_path.open('wb') as output:
    output.truncate(COMPRESSED_SIZE)


def download(chunk):
    position, length = chunk
    data = fetch(start + position, start + position + length - 1)
    with compressed_path.open('r+b') as output:
        output.seek(position)
        output.write(data)
    return length


completed = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    for length in executor.map(download, chunks):
        completed += length
        print(f'Downloaded {completed}/{COMPRESSED_SIZE}', flush=True)

inflater = zlib.decompressobj(-15)
with compressed_path.open('rb') as source, (ROOT / 'results.db').open('wb') as target:
    while block := source.read(4 * 1024 * 1024):
        target.write(inflater.decompress(block))
    target.write(inflater.flush())
if not inflater.eof:
    raise RuntimeError('Incomplete deflate stream')
print(f'Extracted {ROOT / "results.db"}', flush=True)
