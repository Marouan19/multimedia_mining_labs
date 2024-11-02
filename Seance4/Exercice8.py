class WaveCipher:
    def __init__(self, key_size):
        self.key_size = key_size
        self.wave_parameters = self._generate_parameters()

    def encrypt(self, data):
        blocks = self._preprocess(data)
        waves = [self._to_wave(block) for block in blocks]
        encrypted = [self._apply_key(wave) for wave in waves]
        return self._combine_blocks(encrypted)

    def decrypt(self, cipher_text):
        waves = self._split_blocks(cipher_text)
        decrypted = [self._remove_key(wave) for wave in waves]
        return self._postprocess(decrypted)