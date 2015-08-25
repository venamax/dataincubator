from __future__ import absolute_import

import typecheck
import fellow

test_data = [
    u"2000 01 01 00   -11   -72 10197   220    26     4     0     0 bos",
    u"2000 01 01 01    -6   -78 10206   230    26     2     0 -9999 bos",
    u"2000 01 01 02   -17   -78 10211   230    36     0     0 -9999 bos",
    u"2000 01 01 03   -17   -78 10214   230    36     0     0 -9999 bos",
    u"2000 01 01 04   -17   -78 10216   230    36     0     0 -9999 bos",
]

@fellow.batch(name="ts.month_hour_model")
@typecheck.test_cases(line=test_data)
@typecheck.returns("number")
def month_hour_model(line):
    return 0

@fellow.batch(name="ts.fourier_model")
@typecheck.test_cases(line=test_data)
@typecheck.returns("number")
def fourier_model(line):
    return 0
