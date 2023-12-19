![2023-12-19_13-08](https://github.com/DarioH0/ProxyMe/assets/123750271/5a1ba589-21bf-4b0f-8217-762ed953c2e2)
# ProxyMe 
A lightweight and versatile proxy server written in Python. It supports various proxy types, including HTTP, HTTPS, SOCKS4, and SOCKS5. This proxy server is designed to be user-friendly and can be easily deployed on any Python-supported device!

Note: SOCKS4 and SOCKS5 features are currently placeholders as I have not finished making them yet.


# Quick Testing Script
```py
import requests

proxy = "https://0.0.0.0:8080" # Change accordingly
url = "https://www.google.com" # >>

proxies = {'http': proxy, 'https': proxy}

try:
    response = requests.get(url, proxies=proxies)
    print(f"Status Code: {response.status_code}\nResponse Content:\n{response.text}")
except requests.RequestException as e:
    print(f"Request failed: {e}")

```
