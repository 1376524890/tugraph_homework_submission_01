#include <iostream>
#include <vector>
#include <queue>
#include <unordered_set>
#include <string>
#include "lgraph.h"
#include "tools/json.hpp"

using namespace lgraph_api;
using json = nlohmann::json;

extern "C" LGAPI bool Process(GraphDB& db, const std::string& request, std::string& response) {
    // 1. 解析输入 JSON，获取起始顶点 ID
    int64_t start_vid = 0;
    try {
        json input = json::parse(request);
        if (input.contains("times")) {
            start_vid = input["times"].get<int64_t>();
        }
    } catch (const std::exception& e) {
        response = std::string("JSON parse error: ") + e.what();
        return false;
    }

    // 2. 创建只读事务
    auto txn = db.CreateReadTxn();

    // 3. BFS 遍历
    std::unordered_set<int64_t> visited;
    std::queue<int64_t> queue;
    std::vector<int64_t> bfs_order;

    visited.insert(start_vid);
    queue.push(start_vid);

    while (!queue.empty()) {
        int64_t current_vid = queue.front();
        queue.pop();
        bfs_order.push_back(current_vid);

        auto vertex = txn.GetVertexIterator(current_vid);
        if (!vertex.IsValid()) continue;

        for (auto edge_it = vertex.GetOutEdgeIterator(); edge_it.IsValid(); edge_it.Next()) {
            int64_t dst_vid = edge_it.GetDst();
            if (visited.find(dst_vid) == visited.end()) {
                visited.insert(dst_vid);
                queue.push(dst_vid);
            }
        }
    }

    // 4. 释放事务（只读查询推荐 Abort）
    txn.Abort();

    // 5. 构造返回结果
    response = "[";
    for (size_t i = 0; i < bfs_order.size(); ++i) {
        if (i > 0) response += ", ";
        response += std::to_string(bfs_order[i]);
    }
    response += "]";

    return true;
}
