Delay Embedding
===============

**Author:** seberg

**Submitted on:** 2011-07-21 01:43:29-07:00

After having often hacked some odd things to do delay embedding, I found stride_tricks which nicely does the trick and only actually creates a copy when necessary.

.. literalinclude:: /Data/code/2011/07/000007/delay_embedding.py
	:language: python

