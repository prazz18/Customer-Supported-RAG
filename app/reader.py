# this file deals with reading the file from file path and storing it after creating a id for it.
# 1. reading as binary from file path
# 2. decoding the binary as text
# 3. storing the file as (id, file_name, text_content)

from hashlib import sha256
from pathlib import Path
from dataclasses import dataclass

MAX_BYTES = 1_000_000

@dataclass(frozen = True)
class Document : 
    id: str
    source: str
    txt: str


def read_doc(path: str) -> Document :
    #extracting the path 
    file_path = Path(path)
    print(file_path)
    print(file_path.name)
    print(file_path.suffix)
    # rb : read-binary,     content stores the bytes
    with file_path.open("rb") as stream:
        content = stream.read(MAX_BYTES + 1) 
    # reading the doc
    name = file_path.name
    # chk if type of file is in {.txt, .md}
    if file_path.suffix.lower() not in {'.txt', '.md'} : 
        raise ValueError('File type not supported')
    if not content or len(content) > MAX_BYTES : 
        raise ValueError('File too long')
    # print(content)
    #decoding the content in readable text
    try: 
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError as exc:
        raise ValueError('Save the text file as UTF-8') from exc

    # print(repr(text))
    text = text.replace('\r\n', '\n')
    text = text.replace('\r', '\n').strip()

    if not text or '\x00' in text: 
        raise ValueError('Empty binary')
    if len(text) > MAX_BYTES: 
        raise ValueError('File too long')

    # to encode the file : same name && content => then only same result.
    id = sha256(name.encode() + b"\0" + content).hexdigest()
    print(id)
    return Document(id, name, text)


if __name__ == "__main__" : 
    val = read_doc('../data/taskflow.txt')
    print(val)