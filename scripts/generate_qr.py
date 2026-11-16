"""Generate print-ready QR assets. Requires qrcode==8.2; no network at runtime."""
from pathlib import Path
import struct
import zlib
import qrcode
import qrcode.image.svg

URL = 'https://takashithotec.github.io/randomness-lab/'
out = Path(__file__).resolve().parents[1] / 'assets'
out.mkdir(exist_ok=True)
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=20, border=4)
qr.add_data(URL)
qr.make(fit=True)
qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage).save(out / 'randomness-lab-qr.svg')
matrix = qr.get_matrix()
scale = 24
side = len(matrix) * scale
raw = bytearray()
for row in matrix:
    scanline = b'\x00' + b''.join(bytes([0 if cell else 255])*scale for cell in row)
    raw.extend(scanline * scale)
def chunk(kind, payload):
    return struct.pack('!I', len(payload)) + kind + payload + struct.pack('!I', zlib.crc32(kind+payload)&0xffffffff)
png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('!IIBBBBB', side, side, 8, 0, 0, 0, 0))
png += chunk(b'pHYs', struct.pack('!IIB', 11811, 11811, 1))
png += chunk(b'IDAT', zlib.compress(bytes(raw), 9)) + chunk(b'IEND', b'')
(out / 'randomness-lab-qr.png').write_bytes(png)
assert all(not value for row in matrix[:4] for value in row)
assert all(not value for row in matrix[-4:] for value in row)
assert qr.data_list[0].data.decode() == URL
print(f'QR generated: {URL}; version {qr.version}; {side}x{side}px; 4-module quiet zone; EC=M')
