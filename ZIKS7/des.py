import os
import pyDes
import time
import secrets
from docx import Document


def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()


def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)


def des_encrypt(key, data):
    start_time = time.perf_counter()
    k = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Encryption time: {duration} seconds")
    return k.encrypt(data)


def des_decrypt(key, encrypted_data):
    start_time = time.perf_counter()
    k = pyDes.des(key, pyDes.CBC, "\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"Decryption time: {duration} seconds")
    return k.decrypt(encrypted_data)


def main_sender_1():
    txt_file_path = 'txt_file.txt'
    sender_first_key = secrets.token_bytes(8)
    txt_data = read_file(txt_file_path)
    encrypted_txt_data = des_encrypt(sender_first_key, txt_data)
    write_file('encrypted_txt_file.txt', encrypted_txt_data)
    print("Encrypted txt file ready for exchange.")
    return sender_first_key, 'encrypted_txt_file.txt'


def main_receiver_2(sender_des_key, encrypted_txt_file):
    print("Encrypted txt file received.")
    decrypted_txt_data = des_decrypt(sender_des_key, read_file(encrypted_txt_file))
    write_file('decrypted_txt_file.txt', decrypted_txt_data)
    print("Txt file decrypted successfully.")
    docx_file_path = 'docx_file.docx'
    docx_data = read_file(docx_file_path)
    sender_second_key = secrets.token_bytes(8)
    encrypted_docx_data = des_encrypt(sender_second_key, docx_data)
    write_file('encrypted_docx_file.docx', encrypted_docx_data)
    print("Encrypted docx file ready for exchange.")
    return sender_second_key, 'encrypted_docx_file.docx'


def main_receiver_1(sender_des_key, encrypted_docx_file):
    print("Encrypted docx file received.")
    decrypted_docx_data = des_decrypt(sender_des_key, read_file(encrypted_docx_file))
    write_file('decrypted_docx_file.docx', decrypted_docx_data)
    print("Docx file decrypted successfully.")


if __name__ == "__main__":
    # Перший абонент шифрує текстовий файл та передає другому абоненту разом з ключем
    sender_des_key, encrypted_txt_file = main_sender_1()

    # Другий абонент отримує зашифрований текстовий файл та ключ та розшифровує його, а потім шифрує документ MS Word та передає назад разом з новим ключем
    receiver_des_key, encrypted_docx_file = main_receiver_2(sender_des_key, encrypted_txt_file)

    # Перший абонент отримує ключ і зашифрований документ MS Word і розшифровує документ
    main_receiver_1(receiver_des_key, encrypted_docx_file)
