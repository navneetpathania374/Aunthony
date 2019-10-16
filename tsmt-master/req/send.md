

# User story for sending


Users will want to send several ways
- send bitcoin to someone using the address 
- send bitcoin to someone using a qr code (uploaded) in various formats 
- send stellar/stellar asset to someone using address
- send stellar/stellar asset to someone using federation
- send setellar/stellar asset to someone using qr code address
- send stellar/stellar asset to someone using qr code sep-007
- send stellar/stellar asset to an exchange with a memo (need to validate)
- send to a contact

### Phase 2
- send to an email address
- send to a phone number
- default setting in preferences is to send an email with an approval after each send if over a given amount

### function requirements
- Wallet must support Federation lookup (SEP-0002)
- https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0002.md
- Wallet should guard against sending funds to exchanges without memos.
- wallet should try to validate the address
- https://www.stellar.org/community/wallet-guidelines

In general the person will know what they need to send. We can ask them 

### stellar federation

if the address contains a star and a domain then it is a federation call. This should result in a stellar address and memo
- https://github.com/antb123/stcli/blob/master/stcli.py#L299
- https://YOUR_FEDERATION_SERVER/federation?q=jed*stellar.org&type=name
- https://www.stellar.org/developers/guides/concepts/federation.html

```json
{
  "stellar_address": <username*domain.tld>,
  "account_id": <account_id>,
  "memo_type": <"text", "id" , or "hash"> *optional*
  "memo": <memo to attach to any payment. if "hash" type then will be base64 encoded> *optional*
}```


### if this is a bitcoin address
https://stackoverflow.com/questions/21683680/regex-to-match-bitcoin-addresses
^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$

- needs to work with bitcoin testnet if setting is "TEST"


### if this is a qr code
1) ask what crypto
2) decode it and fill in destination