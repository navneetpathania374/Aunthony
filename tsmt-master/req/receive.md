

# User story for receiving


Users will receive in several ways
- receive bitcoin from someone using their wallet address 
- receive bitcoin from using a qr code (uploaded) in various formats 
- receive stellar/stellar asset to someone using address
- receive stellar/stellar asset to someone using federation
- receive setellar/stellar asset to someone using qr code address
- receive stellar/stellar asset to someone using qr code sep-007
- receive stellar/stellar asset to an exchange with a memo (need to validate)
- receive from an email address (send either a btc request, stellar formatted address or their public key)



### function requirements
- Wallet must display public btc address once requested using naobtc.com deposit service
- format for stellar requests: 
- https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0006.md

```
Request to include in the email:


Example 1 - Request for a payment with lumens:

web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.1234567&memo=skdjfasf&msg=pay%20me%20with%20lumens

Example 2 - Request for a payment with a specific asset:

web+stellar:pay?destination=GCALNQQBXAPZ2WIRSDDBMSTAKCUH5SG6U76YBFLQLIXJTF7FE5AX7AOO&amount=120.123&asset_code=USD&
asset_issuer=GCRCUE2C5TBNIPYHMEP7NK5RWTT2WBSZ75CMARH7GDOHDDCQH3XANFOB&memo=hasysda987fs
```



### Django stellar federation

The federation call should be done using django rest framework.



username*qwallet.tempo.eu.com

- https://YOUR_FEDERATION_SERVER/federation?q=jed*stellar.org&type=name
- https://www.stellar.org/developers/guides/concepts/federation.html

```json
{
  "stellar_address": <username*domain.tld>,
  "account_id": <account_id>
}```


