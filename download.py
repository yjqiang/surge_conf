import os
import shutil

import requests
import toml

import setting


if __name__ == "__main__":
    # 清空 download 文件夹
    shutil.rmtree(setting.DOWNLOAD_PATH)
    os.mkdir(setting.DOWNLOAD_PATH)
    
    with open(f'{setting.CONF_PATH}/download.toml', 'r', encoding='utf8') as f:
        result = toml.load(f)
        dict_urls = result['urls']
    
    with requests.Session() as ss:
        for name, url in dict_urls.items():
            text = ss.get(url).text
            with open(f'{setting.DOWNLOAD_PATH}/{name}.conf', 'w', encoding='utf8') as f:
                # 特殊处理
                if name == 'rule':
                    f.write('[Rule]\n')
                f.write(text)

