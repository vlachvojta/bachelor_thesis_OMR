# Transformer errors

## number of dims don't match in permute


Traceback (most recent call last):
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/train_pytorch_ocr.py", line 1010, in <module>
    main()
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/train_pytorch_ocr.py", line 393, in main
    _, loss = model_wrapper.train_step(batch)
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/transformer.py", line 305, in train_step
    out, loss = self.forward_pass(batch)
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/transformer.py", line 328, in forward_pass
    logits = self.net.forward(inputs, input_labels)
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/transformer.py", line 213, in forward
    encoder_output = self.encode(X)
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/transformer.py", line 230, in encode
    enc = self.encoder(enc)
  File "/afs/.ics.muni.cz/software/python36-modules/gcc/lib/python3.6/site-packages/torch/nn/modules/module.py", line 889, in _call_impl
    result = self.forward(*input, **kwargs)
  File "/scratch.ssd/xvlach22/job_14552065.meta-pbs.metacentrum.cz/code_from_others/pero-transformers/pytorch_ctc/transformer.py", line 55, in forward
    image_enc_tbc = X.permute(2, 0, 1)  # [time, batch, channels]
RuntimeError: number of dims don't match in permute