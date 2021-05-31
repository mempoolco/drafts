```
  
  Title: Distributing the UTXO set over torrent
  Author: Guido Dassori <....>
  Comments-Summary: None yet
  Comments-URI: 
  Status: Draft
  Type: 
  Created: 2021-05-24
  License: CC0-1.0
```


#### Assumptions:

- At the time of writing the UTXO set for Bitcoin is around 4GB.
- Without investigating further, we assume a set of related proofs for the UTXO is 4x.
- Today a lot of light clients relays on custodians, indexes services (electrum), or explorers.

#### Proposal:

- To split the UTXO set into 1024 shard.
- To organize those 1024 shard by doing, for every shard, a modulus operation `dblsha256(scriptPubKey) % shards_count`, and put the related utxo in the relative shard.
- To use a wide adopted protocol, BitTorrent, to share the shards across public trackers. 
- That a patch protocol is established for incremental updates.
- That clients consuming those torrents would share 2:1 the downloaded shards, for privacy improvements and network health.
- That clients adopting this protocol use a certain scheme for address generation.

#### Reducing fragmentation:

To benefit from this proposal, a wallet must reduce the fragmentation of its utxo allocation in the index.
The modulus-based utxo organization must be adopted by the clients as well, by brute-forcing ECDH paths, "sharded scripts" from now.

A sharded script is generated as follows:

```
fragmentation_set = {0...1023} 
n = ...
while 1 {
 scripthash = scripthash[bip44path[n]]
 fragmentation_idx = scripthash % 1024
 if fragmentation_idx in fragmentation_set {
   break 
 }
 n += 1
}
```

Regarding the distribution and seeding:

```
Needs 8 subsets = 160MB
Shares 2:1 subsets = 320MB
```
those figures should be enough to validate the UTXO set and improve the privacy, compared to using conventional utxo indexing.

Using an 8-on-1024 addresses subset means discarding 1016 scripts on average, leading to slow addresses generation. 
Even increasing the defragmentation to 200% or 1000% doesn't seem to improve this side, as with a subset size of 80 a client should still discard nearly 1000 scripts.

On the privacy side, instead, increasing the seed ratio leads to a drastic improvement, as every shard is supposed to hold roughly 80.000 scripts at the time of writing, having 8 shards would mean tracking 640.000 possible outputs.

To address the slow addresses generation issue, a pool of "sharded scripts" could be generated in advance, using idle times.


#### Authoring and distribution of the UTXO set:

At the time of writing, indexing services (Electrum-like indexers or block explorers) account a lot of the network traffic.
BIP-37 is slowly going to deprecation. In opposition to the current centralization of indexing services, with this proposal:

- Anyone could author a UTXO set and sign it with an ECC signature.
- Anyone could verify the set using a full node.
- All the legit sets shards authored at the same blockhash, must hash in the same way.
- Some metadata could be added to the set, with no hash invalidation, but committed to the signature.
- The shards hash, put into a Merkle tree and committed to the blockhash at which they are authored, leads to fast verification.
- Incremental updates are possible by patch files.
- Various methods, OP return, 0fee txs unlikely to be mined, DNS seeding w/ DNSSEC, could be used to obtain magnet links of the utxo set.

#### Cons:

- Peers must advertise themselves.
- Brute force ECDH to avoid utxo fragmentation probably breaks existing BIPS.


Copyright
---
This document is licensed under the Creative Commons CC0 1.0 Universal license.
