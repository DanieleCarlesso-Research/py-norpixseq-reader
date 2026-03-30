import numpy as np
import cv2


SOI = b'\xff\xd8'  # Start of Image
EOI = b'\xff\xd9'  # End of Image

class JPEGSeq:
    def __init__(self, path, header_size=1024, max_frames=None):
        self.path = path
        self.header = header_size
        self.frame_offsets = []
        self._scan(max_frames=max_frames)

    def _scan(self, chunk_size=8 * 1024 * 1024, max_frames=None):
        print("Scanning JPEG frames (streaming)...")
        self.frame_offsets = []
        with open(self.path, "rb") as f:
            f.seek(self.header)
            buffer = b''
            pos_global = self.header

            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                data = buffer + chunk
                i = 0

                while True:
                    soi = data.find(b'\xff\xd8', i)
                    if soi == -1:
                        break
                    eoi = data.find(b'\xff\xd9', soi)
                    if eoi == -1:
                        break

                    start = pos_global - len(buffer) + soi
                    end   = pos_global - len(buffer) + eoi + 2
                    self.frame_offsets.append((start, end))
                    i = eoi + 2

                    if max_frames and len(self.frame_offsets) >= max_frames:  # ← early exit
                        print(f"Done. Frames found (capped): {len(self.frame_offsets)}")
                        return

                buffer = data[-1024:]
                pos_global += len(chunk)

        print("Done. Frames found:", len(self.frame_offsets))

    def __len__(self):
        return len(self.frame_offsets)

    def __getitem__(self, idx):
        start, end = self.frame_offsets[idx]
        with open(self.path, "rb") as f:
            f.seek(start)
            buf = f.read(end - start)
        # decode JPEG
        img = cv2.imdecode(np.frombuffer(buf, np.uint8), cv2.IMREAD_GRAYSCALE)
        
        return img