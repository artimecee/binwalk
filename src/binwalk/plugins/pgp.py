#!/usr/bin/env python

import errno
import shutil
import tempfile
import binwalk.core.plugin
import binwalk.core.compat
import binwalk.core.common
try:
    # Requires the python-gnupg library
    from gnupg import GPG
except ImportError as e:
    GPG = None


class PgpDecryptor(binwalk.core.plugin.Plugin):

    '''
    Plugin to decrypt, validate, and extract PGP encrypted firmware.
    '''
    MODULES = ["Signature"]

    EDDA2E82EDC7030C_KEY = """-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=c6nn
-----END PGP PRIVATE KEY BLOCK-----"""

    F18B47DF3F881C75_KEY = """-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=UtFV
-----END PGP PRIVATE KEY BLOCK-----"""

    _6F6BE91DF2D929B6_KEY = """-----BEGIN PGP PRIVATE KEY BLOCK-----

lQOYBE8fGU8BCACjfpRQ5T//ZGS5yHCMx4sktUxW2VQD0sknLJihOuQTX7IsNsTe
qvYY1C7GoGRX147CSYpteW1/nWnrTSncqjGaYNgbbJz43dIrPfJPJT4rH2YyaPxJ
jyayeS+/zZBtkS2MIQ+G6MwxH2BgY/w9anSgpkgsfwX8YZ2cJbJEhXUm7trZQa2Q
ctUuiNm3/s4WN9ZhIRlBYG0UkdGrDn4ietfU+Am5fRrkRtkN3sRSkTrtth1TS7Bk
kFkrS6Ncw3FXnrQW8Y0Cktblb4EN82DIyTgFX5e7b0FLXMriTBnUzFNB6zuAZphF
donc5duPsuI/oZJuya/Dq8TPha6zf6ftTDqhABEBAAEAB/4lH8SrUsbzpbb2dZRS
7yuB+BXfwaUBYj9RQR/eOmpYGNpzDjOpUP4lGKcPbJOkW5q7tKm1XoV13QdUSfb3
t4Cgap2fqovBOdMzhPMstAr4DT7uMucYh+QUUg682X9SVc0XHNmy+1EEVXjToliA
FJhrcx5/1g8EpiC8+FVQmFJH9scVEPArsdU7VW4+1SC9vhBoO8IoTVODS6oQj/wx
EnyHJQVyghofaOaeU7TtPhcUjKLcPc8Z1Pm/PICp9WnJdqtE5W6x4uYhAoAivANw
irtexg+TsnG+cu1LqHp3JIiYZkgyzMOB8dw56GQ0hO/0vpKwkCv0g0DUIq60Lt8w
ywI9BADBR9+cOPZbl//5BLOCuKPe4dBJoJwtHORerX/e66ykXlW6LiUvRFVe4Cb6
NVjYJMNaUe1ZXM/fsRStu5wuS/+Dbp6FRiKKjaVFFB2XmGCOcY30h3o0UPFIsdvg
uARO8YNm7Q5R3FXtWBIe7YiPeNjM2v39ifooenESJHLgWFQuvQQA2IxP60CZB1Yx
dcaaKfbQ1z/v/+KgxayyIpN7w2LrTEWgZTPDSi8zHCcHbhjQ57e2K6gfGcXVX+fw
VbrIx5Ly6HbwqI5JPSZre5VvyYPW+RJcKFBwxBvWfkLd1DcxKBfGoRuF9eXPyP8c
kC2zFQlgQuKH/5MocBWPDAtRWAFyW7UEAMMabCtXC9HAX3yts0WqqsmETkouNknx
J20eVdHK38EKE0ZJiQGL9SWMcBGFIcOlCJWVome4SYHh5LFcicK5r/d4TYbeTKBh
I24rQw0+IQ3ZRxi58Am9yMjN56nxfuQ/sUfqaEeVnsBhp2xYUzXOztAimQNxOFbS
FxsE7CZuaHGfQIG0OWlDb250cm9sIFRvdWNoc2NyZWVuIChVcGdyYWRlKSA8dG91
Y2hzY3JlZW5AaWNvbnRyb2wuY29tPokBOAQTAQIAIgUCTx8ZTwIbAwYLCQgHAwIG
FQgCCQoLBBYCAwECHgECF4AACgkQvlUh4ddQaieDuQf/ftaApP/ZUtYhN8iPSCwz
oa8YbNjxxbbqkrbe4j/uIgLuXbfnHQ2xQ9o37NDBIe0GFakBWUaLi9WSzRnWOc5A
O0G0uSscYl8uWG/i/+Sl2kjmQfvGXS6CtKGvwjBtXEMUist/fg0fJlDzGu60sen7
C9NVn1ZZSA1SAA2WVXHV7XDNvgy4x3MoV2yAZceorZTQ1BHLEslesRSd9t8sLuQz
2cxvcH/El6mrJKjcPaogJUyLxJHIxXv1Ljp6XV3yLVLp22+cMcPuc7mopqtwDw89
u8nTP14wkKsSGmY3P9ZtuwP970oIvAibUGIBdei+UZG3bqRja8s+F6G8YN3tCiGI
5Z0DmARPHxlPAQgA4DtGlKmS17tldfwqEnimhI1tmIp3GiVoYdbBbbaPYv+42qfn
iHjn+tha02oJFLYkVvxKFpBm9PF+hRm//ZXccE43oBWQANdJQVGbckdLbOudbdYv
9J+92s6FOXPyDgdk5pWFs7yLBvPX20iZsNvSpdEZ4zuUioGErX1i8/arhyq82BXw
uNdBs6O4AA+pbdiO5IhDVn9VtWacoN3omZSC5FFfhHA+8Xw7K5kBdAUOqm0SaAc1
Bz62aMSMVOVKsXF9Hh2g31bLAFXzfX752OIVQ0qNKc8sCvxGTQJ9SpV5cE8LFyZu
TB25dA3Aq/5j+94Z9njcgIDLmjMn30t6xINjmQARAQABAAf7BVCyZBy+69k31vui
vaxZeiPmGKsTlq2TU1plXGXq8TRRm/FF9kCzcwlE4eUOEQ0eQGebk/xZTG4bCymo
mOjAAHOCMwu/zZ1M0b0O+77/5TWSlkNxAJH2zKR/mPSMJNP9CtA5iqCqBQCrubl3
Vy9mx2J1BCNp6nyWegxSV6kduMb5swWbB4Hgsqh4p+FPAv81pCF0w/LWUtUugj1W
ZLsz6xz6P0KBjQDN09aTfAmTAHXOl08uj/Oy6f+asDOQ6Si6EcjmDIH59V1w514a
+qdN1G0A76N5osn6mqSxgy0zxG/t1TvtEsxlmH8twFUzM64EBoHZLIwdthB5avgM
iT1ZDwQA5LUJtqnTpilEVnHegj7buz0UVvygxYzolCaaXw1OWQbg0Yqe4aE866MB
mZSh72u8kd3AoILwMgKtaWfFN4hYe2epmFH8h9vezguUbgTIbSqbQ6SHvQQWHTaT
iASntIvIQih1VXtWDsGlgwyazwxfl7fU6JGz81QDY0VtJZ59CacEAPr9ggrpC6X/
rLKn/MSW2clMeSGX+l4d3NAh9k/HK5uZkEyuI0vDDAG6yR5wuLk8FZeCUiL0fC+V
DWISkqrP13cfgvloMD8hmSGFhkwYRrquAtuqSfFU6GccURsIA9wv97QPRwEhnSsq
578lH5m79jG9y81Ok8kAXii4Rw4ow1C/BACsaR07Cyt16KXmzq3zSEHcg0EEHbpm
pSb/AgdBoBJ9HBmRxInl3bAtYEY8Ikwo5XYFQ5NeAlkSLf1Pw02AlCU/R5iGR070
T07tQTsxYASlZZHxRjFYGQfb48OJ7F+2mVBxPpouTeNUGG1E8tQG+djZbcBNWLOI
foxV9fRfnvvdfDpqiQEfBBgBAgAJBQJPHxlPAhsMAAoJEL5VIeHXUGonoGoH/RsH
m/M3uy1aZU6ke1wNiJaQAKF4BUGhvsfeGfHmUhXVN2bsWjxcN+3ECyfB04x08N5S
EZ+iVCG3Wqe1xrzFCLac+KiGeqJxSFrWaN3eYlchRk9ZKUX9rgBfwCzEE1NEWrkJ
nd8yGbCfC2XpbNbBfJoDsVyrfkAP0nT24UHK3BAAUp2glhguKtlXZme9oFy8AtOY
w2H5LPbdUkM/00bkbNPeiRDDw26dQ/BB/PNC1KXBSM0d8dCgzBF+L3cSAK3NrpcW
fYalnt/6kLvkRZzYqO2lUSkVTeTpZ9CdnEjZG6H3M9NeL3wtrktHbAW3gWuI9Vql
ZKRdu7NkEp9EYhvl/vM=
=vnXr
-----END PGP PRIVATE KEY BLOCK-----"""

    EDDA2E82EDC7030C_SIGNATURE_DESCRIPTION = "PGP RSA encrypted session key - keyid: EDDA2E82 EDC7030C RSA".lower()

    F18B47DF3F881C75_SIGNATURE_DESCRIPTION = "PGP RSA encrypted session key - keyid: F18B47DF 3F881C75 RSA".lower()

    _6F6BE91DF2D929B6_SIGNATURE_DESCRIPTION = "PGP RSA encrypted session key - keyid: 6F6BE91D F2D929B6 RSA".lower()

    def init(self):
        if GPG is None:
            self.enabled = False
        else:
            self.enabled = True

        if self.enabled is True and self.module.extractor.enabled is True:
            # Add extraction rules for encrypted PGP firmware signature
            # results
            self.module.extractor.add_rule(txtrule=None,
                regex="^%s" % self.EDDA2E82EDC7030C_SIGNATURE_DESCRIPTION,
                extension="gpg",
                cmd=self._decrypt_and_extract_EDDA2E82EDC7030C)
            self.module.extractor.add_rule(txtrule=None,
                regex="^%s" % self.F18B47DF3F881C75_SIGNATURE_DESCRIPTION,
                extension="gpg",
                cmd=self._decrypt_and_extract_F18B47DF3F881C75)
            self.module.extractor.add_rule(txtrule=None,
                regex="^%s" % self._6F6BE91DF2D929B6_SIGNATURE_DESCRIPTION,
                extension="gpg",
                cmd=self._decrypt_and_extract_6F6BE91DF2D929B6)

    def _decrypt_and_extract_EDDA2E82EDC7030C(self, fname):
        return self._decrypt_and_extract(fname, self.EDDA2E82EDC7030C_KEY)

    def _decrypt_and_extract_F18B47DF3F881C75(self, fname):
        return self._decrypt_and_extract(fname, self.F18B47DF3F881C75_KEY)

    def _decrypt_and_extract_6F6BE91DF2D929B6(self, fname):
        return self._decrypt_and_extract(fname, self._6F6BE91DF2D929B6_KEY)

    def _decrypt_and_extract(self, fname, key):
        '''
        This does the extraction (e.g., it decrypts the image and writes it to a new file on disk).
        '''
        with open(fname, "rb") as fp_in:
            encrypted_data = fp_in.read()

            decrypted_data = self._pgp_decrypt(encrypted_data, key)

            with open(binwalk.core.common.unique_file_name(fname[:-4], "dec"), "wb") as fp_out:
                fp_out.write(decrypted_data)
        return True

    def _pgp_decrypt(self, encrypted_firmware, key):
        '''
        This does the actual decryption.
        '''
        try:
            tmp_dir = tempfile.mkdtemp()
            gpg = GPG(gnupghome=tmp_dir)
            gpg.import_keys(key)
            decrypted_data = gpg.decrypt(encrypted_firmware)
        finally:
            try:
                shutil.rmtree(tmp_dir)
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise

        return bytes(decrypted_data.data)

    def scan(self, result):
        '''
        Validate signature results.
        '''
        if result.valid is True:
            if result.description.lower().startswith(self.EDDA2E82EDC7030C_SIGNATURE_DESCRIPTION) is True:
                result.description += ", Verizon BHR4 <eu@greenwavereality.com>"
            elif result.description.lower().startswith(self.F18B47DF3F881C75_SIGNATURE_DESCRIPTION) is True:
                result.description += ", Verizon BHR4 <eu@greenwavesystems.com>"
            elif result.description.lower().startswith(self._6F6BE91DF2D929B6_SIGNATURE_DESCRIPTION) is True:
                result.description += ", iControl Touchscreen (Upgrade) <touchscreen@icontrol.com>"
