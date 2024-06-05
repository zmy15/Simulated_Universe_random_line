import base64
import json

# 读取角色信息 JSON 文件
with open('characters.json', 'r', encoding='utf-8') as f:
    characters = json.load(f)

# 编码角色信息 JSON
characters_json_base64 = base64.b64encode(json.dumps(characters, separators=(',', ':')).encode('utf-8')).decode('utf-8')

# 编码图片
images_base64 = {}
for char in characters:
    with open(char['image'], 'rb') as image_file:
        images_base64[char['name']] = base64.b64encode(image_file.read()).decode('utf-8')

# 读取配置文件
try:
    with open('config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {
        "attributes": [],
        "fates": [],
        "included_names": []
    }

# 编码配置 JSON
config_json_base64 = base64.b64encode(json.dumps(config, separators=(',', ':')).encode('utf-8')).decode('utf-8')

# 生成嵌入数据的 Python 文件
with open('embedded_data.py', 'w', encoding='utf-8') as f:
    f.write("import base64\n")
    f.write("import json\n")
    f.write(f"characters_json_base64 = '{characters_json_base64}'\n")
    f.write(f"images_base64 = {json.dumps(images_base64)}\n")
    f.write(f"config_json_base64 = '{config_json_base64}'\n")
