flag_enc  = "brcfxba_vfr_mid_hosbrm_iprc_exa_hoav_vwcrm"
flag_form = ""

# Ta có mảng thay thế một số chữ, dựa trên phân giải tự động trên link:
# https://www.dcode.fr/monoalphabetic-substitution
original_chars = "sprgwhkjozxldcuvyemnbtiafq"
encrypts_chars = "abcdefghijklmnopqrstuvwxyz"
char_mapping = {encrypts_chars[i]: original_chars[i] for i in range(len(original_chars)) if encrypts_chars[i] != '*'}
# print(char_mapping)

def decrypt_message(cipher, char_map):
    res = []
    for char in cipher:
        if char in char_mapping:
            res.append(char_mapping[char])  # Thay thế ký tự
        elif char.isupper():  # Nếu ký tự là chữ hoa
            if char.lower() not in char_mapping:
                res.append('*')
            else:
                res.append(char_mapping[char.lower()].upper())
        elif char.isalpha():
            res.append('*')
        else:
            res.append(char)  # Giữ nguyên ký tự không phải chữ cái

    return ''.join(res)

print(decrypt_message(flag_enc, char_mapping))