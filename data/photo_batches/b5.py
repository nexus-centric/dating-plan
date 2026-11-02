from add import *
P='https://lh3.googleusercontent.com/'
for i,u in {
156:'grass-cs/AABkmLfzoCgGHuR-lSqGHCYVcxZA7w1DuBwy94A9Czt-TYJlbc140sll6TpaUZjrOG7QYGl1piJx2eyP8OeNTSRlQXp9tJDCE0E6cAgzdUwjx6ipiSZUc-u0-Ve67noQxKQ3j0gmZst5pH4hyrSc=w408-h544-k-no',
157:'grass-cs/AABkmLfgc7xuK7VKdpIay_LD0H_6f307GYUixhHVGpUUBI4XNaUxrk41pF49QFod1e-3Dx4wTmgz7wIjdmT-fOI4s8za1sKGhiSrHRRILTPcDHAbZzDt4pTxRZYAQ_J7nAmV1Bxy4oCT3ZsxZByw=w408-h271-k-no',
158:'grass-cs/AABkmLcZysSTkPix8ZEhjoi2j5c_SJabsKpLhRT7DG0vzug_GewDU-PwtLFX8ZpQc87q0Ui5BNm9PaCUCEvU8s9Q24hm0D77mtU-Fql2b1hJZWSW02OlVcUxsdAXVOmt4KBeVpFOw3ppEuELgZXO=w408-h544-k-no'}.items(): add(i,'ok',P+u)
save()
import collections;print(len(R),collections.Counter(r['status'] for r in R))
