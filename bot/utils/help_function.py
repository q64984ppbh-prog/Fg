import base64

def encode_referral(user_id: int) -> str:
    return base64.urlsafe_b64encode(str(user_id).encode()).decode().rstrip("=")

def decode_referral(ref_code: str) -> int | None:
    try:
        padding = "=" * (-len(ref_code) % 4)
        return int(base64.urlsafe_b64decode(ref_code + padding).decode())
    except Exception:
        return None

def clean(get_text: str) -> str:
    if get_text is not None:
        split_text = get_text.split("\n")

        if split_text[0] == "": split_text.pop(0)
        if split_text[-1] == "": split_text.pop(-1)
        save_text = []

        for text in split_text:
            while text.startswith(" "):
                text = text[1:]

            save_text.append(text)
        get_text = "\n".join(save_text)
    else:
        get_text = ""

    return get_text