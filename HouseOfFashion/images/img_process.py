# functions to deal with images
import hashlib


def hash_md5(file):
    """
    返回文件file的md5值
    :param file: 文件
    :return: md5值
    """
    hasher = hashlib.md5()
    # chunks()是方法，之前把括号漏了
    for chunk in file.chunks():
        hasher.update(chunk)

    return hasher.hexdigest()
