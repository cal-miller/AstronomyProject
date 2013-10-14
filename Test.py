import time
import sys
sys.stdout.write(' ')
while True:
    for c in ('/', '-', '\\', '|'):
        time.sleep(1)
        sys.stdout.write('\r' + c)
        sys.stdout.flush()