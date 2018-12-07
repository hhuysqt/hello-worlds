Embedded Zerotree Wavelet(EZW)
===

Paper
---
[Embedded Image Coding Using Zerotrees of Wavelet Coefficients](https://pdfs.semanticscholar.org/d0e7/101bf2b01f2e76a56bed18848e0d08f261b6.pdf)

Implementation
---
Things different form the classical EZW algorithm:
- Encode each bitwise band instead of a weight approximation.
- Take the wavelet result as a `heap` of quadtree, and iterate it in first-root order, instead of the original zigzag scheme.

![heap scheme](https://github.com/hhuysqt/hello-worlds/raw/master/ezw/quadheap.jpeg)