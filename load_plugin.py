"""
加载/调用/删除 TuGraph C++ 存储过程 (v1)
默认连接本地 TuGraph，也可通过命令行指定远程地址
"""
import requests
import json
import base64
import sys

# 默认连接本地 Docker 容器中的 TuGraph
BASE_URL = "http://127.0.0.1:7071"
DB = "default"
PLUGIN_NAME = "ceshi_BFS"
PLUGIN_SO = "ceshi_BFS.so"


def load_plugin(so_path=PLUGIN_SO, name=PLUGIN_NAME, db=DB, read_only=True):
    """将 .so 文件加载为 C++ 存储过程"""
    with open(so_path, "rb") as f:
        code = f.read()

    data = {
        "name": name,
        "code_base64": base64.b64encode(code).decode(),
        "description": "BFS traversal from given start vertex",
        "read_only": read_only,
        "code_type": "so",
    }
    url = f"{BASE_URL}/db/{db}/cpp_plugin"
    r = requests.post(url, data=json.dumps(data),
                      headers={"Content-Type": "application/json"})
    print(f"[LOAD] status={r.status_code}, body={r.text}")


def list_plugins(db=DB):
    """列出所有已加载的 C++ 存储过程"""
    url = f"{BASE_URL}/db/{db}/cpp_plugin"
    r = requests.get(url)
    print(f"[LIST] status={r.status_code}")
    if r.status_code == 200:
        plugins = r.json().get("plugins", [])
        for p in plugins:
            print(f"  - {p['name']}: {p.get('description', '')}, read_only={p.get('read_only', '')}")


def call_plugin(input_data, name=PLUGIN_NAME, db=DB):
    """调用 C++ 存储过程"""
    url = f"{BASE_URL}/db/{db}/cpp_plugin/{name}"
    r = requests.post(url, data=json.dumps(input_data),
                      headers={"Content-Type": "application/json"})
    print(f"[CALL] status={r.status_code}")
    print(f"  result: {r.text}")


def delete_plugin(name=PLUGIN_NAME, db=DB):
    """删除存储过程"""
    url = f"{BASE_URL}/db/{db}/cpp_plugin/{name}"
    r = requests.delete(url)
    print(f"[DELETE] status={r.status_code}, body={r.text}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 load_plugin.py [load|list|call|delete] [args...]")
        print("  load              - load ceshi_BFS.so into TuGraph")
        print("  list              - list all loaded plugins")
        print("  call <start_vid>  - call BFS with start vertex id (default 100)")
        print("  delete            - remove the plugin")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "load":
        so = sys.argv[2] if len(sys.argv) > 2 else PLUGIN_SO
        load_plugin(so)
    elif cmd == "list":
        list_plugins()
    elif cmd == "call":
        vid = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        call_plugin({"times": vid})
    elif cmd == "delete":
        delete_plugin()
    else:
        print(f"Unknown command: {cmd}")
