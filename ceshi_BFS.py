# coding=utf-8

import json

def Process(db, input):
    # 1. 解析输入参数（默认输入为起始顶点ID，例如 "100" 或 "100,200"）
    raw_data =input
    parsed_data = json.loads(raw_data)
    if "times" in parsed_data:
        start_vid = int(str(parsed_data["times"]))

    # 2. 创建只读事务
    txn = db.CreateReadTxn()

    # 3. BFS 核心逻辑
    visited = {start_vid}
    queue = [start_vid]  # 生产环境建议改用 collections.deque 提升出队性能
    bfs_order = []

    while queue:
        current_vid = queue.pop(0)
        bfs_order.append(current_vid)

        vertex = txn.GetVertexIterator(current_vid)
        if not vertex.IsValid():
            continue

        # 遍历当前顶点的出边迭代器
        edge_it = vertex.GetOutEdgeIterator()
        while edge_it.IsValid():
            dst_vid = edge_it.GetDst()
            if dst_vid not in visited:
                visited.add(dst_vid)
                queue.append(dst_vid)
            edge_it.Next()

    # 4. 释放只读事务资源（只读查询推荐用 Abort）
    txn.Abort()

    # 5. 返回结果（TuGraph 插件标准格式：成功标志, 结果字符串）
    return (True, str(bfs_order))


