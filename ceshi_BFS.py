import json

def Process(db, input):
    # 1. �������������Ĭ������Ϊ��ʼ����ID������ "100" �� "100,200"��
    raw_data =input
    parsed_data = json.loads(raw_data)
    if "times" in parsed_data:
        start_vid = int(str(parsed_data["times"]))

    # 2. ����ֻ������
    txn = db.CreateReadTxn()

    # 3. BFS �����߼�
    visited = {start_vid}
    queue = [start_vid]  # ��������������� collections.deque ������������
    bfs_order = []

    while queue:
        current_vid = queue.pop(0)
        bfs_order.append(current_vid)

        vertex = txn.GetVertexIterator(current_vid)
        if not vertex.IsValid():
            continue

        # ������ǰ����ĳ��ߵ�����
        edge_it = vertex.GetOutEdgeIterator()
        while edge_it.IsValid():
            dst_vid = edge_it.GetDst()
            if dst_vid not in visited:
                visited.add(dst_vid)
                queue.append(dst_vid)
            edge_it.Next()

    # 4. �ͷ�ֻ��������Դ��ֻ����ѯ�Ƽ��� Abort��
    txn.Abort()

    # 5. ���ؽ����TuGraph �����׼��ʽ���ɹ���־, ����ַ�����
    return (True, str(bfs_order))

