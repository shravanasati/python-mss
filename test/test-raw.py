#!/usr/bin/env python
# coding: utf-8

''' Test raw data.
    Data could be contents of self.image generated by the get_pixels() method.
    Data coulb be contents generated by test-linux.
'''

import mss
import sys

if mss.__version__ < '2.0.0':
     from struct import pack
     from zlib import compress, crc32

     def to_png(data, width, height, output):
          ''' Copied from MSS.to_png(). '''

          len_sl = (width * 3 + 3) & -4
          padding = 0 if len_sl % 8 == 0 else (len_sl % 8) // 2
          scanlines = b''.join(
               [b'0' + data[y * len_sl:y * len_sl + len_sl - padding]
                for y in range(height)])
          zcrc32 = crc32
          zcompr = compress
          b = pack

          magic = b(b'>8B', 137, 80, 78, 71, 13, 10, 26, 10)

          # Header: size, marker, data, CRC32
          ihdr = [b'', b'IHDR', b'', b'']
          ihdr[2] = b(b'>2I5B', width, height, 8, 2, 0, 0, 0)
          ihdr[3] = b(b'>I', zcrc32(b''.join(ihdr[1:3])) & 0xffffffff)
          ihdr[0] = b(b'>I', len(ihdr[2]))

          # Data: size, marker, data, CRC32
          idat = [b'', b'IDAT', b'', b'']
          idat[2] = zcompr(scanlines)
          idat[3] = b(b'>I', zcrc32(b''.join(idat[1:3])) & 0xffffffff)
          idat[0] = b(b'>I', len(idat[2]))

          # Footer: size, marker, None, CRC32
          iend = [b'', b'IEND', b'', b'']
          iend[3] = b(b'>I', zcrc32(iend[1]) & 0xffffffff)
          iend[0] = b(b'>I', len(iend[2]))

          with open(output, 'wb') as fileh:
               fileh.write(
                    magic + b''.join(ihdr) + b''.join(idat) + b''.join(iend))


if len(sys.argv) != 4:
    print('Usage: python {0} data.raw width height'.format(sys.argv[0]))
    sys.exit(1)

with open(sys.argv[1], 'rb') as fileh:
     data = fileh.read()
     width = int(sys.argv[2])
     height = int(sys.argv[3])
     output = '{0}.png'.format(sys.argv[1])
     if mss.__version__ < '2.0.0':
         print('Outdated version of MSS, please `pip install --upgrade mss`')
         to_png(data, width, height, output)
     else:
         mss = mss.MSS()
         mss.to_png(data, width, height, output)
     print('File {0} created.'.format(output))
     sys.exit(0)
     print('Impossible to get contents of "{0}".'.format(sys.argv[1]))
