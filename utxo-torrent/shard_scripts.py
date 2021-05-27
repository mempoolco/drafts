import bitcoin, hashlib, time

def test_hd(shards):
  pk = hashlib.sha256(b'pk1').digest()
  master = bitcoin.bip32_master_key(pk)
  i = 0
  subset = {45, 872}
  start = time.time()
  k = 0
  while 1:
    i += 1
    x = bitcoin.bip32_ckd(master, i)
    z = bitcoin.bip32_extract_key(x)
    y = bitcoin.privtopub(z)
    shard = int.from_bytes(bitcoin.bin_dbl_sha256(bytes.fromhex(y)), 'little') % shards
    if shard in subset:
      print(f'pub: {y}, shard: {shard}, i: {i} - took: {time.time() - start:.4f}')
      start = time.time()
      k += 1
      if k == 5:
        break


"""
Intel(R) Atom(TM) CPU N450   @ 1.66GHz

pub: 0232bde2052c1809e973d52bcf61395b327dbb2a9e7f48ec6244f348feb85804ad, shard: 45, i: 201 - took: 19.4838
pub: 03f49319e72225f4d483e5a4ad6bb4942b2657fd424a972ab39caef316e747c8cd, shard: 872, i: 398 - took: 19.8009
pub: 037f95c03d6de2bb5b99e99e4a66803473efded8ba1ae5463228f5cba2a1763bcc, shard: 45, i: 858 - took: 46.1268
pub: 030b097c4955bed9aa9e68dea4c450d230120e02a9274f1b9b692151ebec74401b, shard: 872, i: 1133 - took: 27.5331
pub: 02104138967fc53e59ed24626677337e38be16e3bfdad374cec8f497b6a370ca81, shard: 872, i: 1172 - took: 3.8966


AMD FX(tm)-8350 Eight-Core Processor

pub: 0232bde2052c1809e973d52bcf61395b327dbb2a9e7f48ec6244f348feb85804ad, shard: 45, i: 201 - took: 2.0260
pub: 03f49319e72225f4d483e5a4ad6bb4942b2657fd424a972ab39caef316e747c8cd, shard: 872, i: 398 - took: 1.9669
pub: 037f95c03d6de2bb5b99e99e4a66803473efded8ba1ae5463228f5cba2a1763bcc, shard: 45, i: 858 - took: 4.5697
pub: 030b097c4955bed9aa9e68dea4c450d230120e02a9274f1b9b692151ebec74401b, shard: 872, i: 1133 - took: 2.7357
pub: 02104138967fc53e59ed24626677337e38be16e3bfdad374cec8f497b6a370ca81, shard: 872, i: 1172 - took: 0.3894
"""
