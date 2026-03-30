# py-norpixseq-reader
Python script to read .seq files from Norpix. The function will scan the full sequence file. Example usage: 

```ruby
from seq_jpeg_reader import JPEGSeq

seq = JPEGSeq('//path/to/seq/file')
```

*Length of the sequence file*
```ruby
total_frames = len(seq)
```
*Shape of frame*
```ruby
frame0 = seq[0]
h, w = frame0.shape[:2]
```
