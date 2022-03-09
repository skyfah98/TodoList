# NoSSLHelper

Unverified http and https context for external devices. Legacy Python that doesn't verify HTTPS certificates by default and Handle target environment that doesn't support HTTPS verification.

### Requirements

- [python](https://www.python.org/downloads/)       version 3.8
- [pip](https://pip.pypa.io/en/stable/installing/)  version 19.3

### Usage
   
Just call `NoSSLHelper` in automated scripts. It will ignore SSL by automatically.


```python
    *** Settings ***
    Library  NoSSLHelper
```
        

