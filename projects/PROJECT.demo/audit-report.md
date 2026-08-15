# PROJECT.demo 发布证据

- Canon 版本：`1`
- SQLite outbox：`47` 条变更
- 结构审计：`exit 0`，`errors=[]`
- 上下文检索：`SUFFICIENT`，返回 `4` 个事件超边，负事实 `3` 条
- Markdown 导出：`exit 0`
- Master Outline SHA-256（本次临时演示输出）：`8e9f46b78cdb62444ae0df0f01cd43aa27567b3aa6f20d1979ba6a4bcd21a8d7`
- 单元测试：`python3 -m unittest discover -s .agents/skills/vnext-outline-agent/scripts -p 'test_*.py' -v`，`34/34 PASS`
- Skill 契约校验：`python3 .agents/skills/vnext-outline-agent/scripts/test_skill_contract.py`，`exit 0`
- 字节码校验：`python3 -m py_compile`，`exit 0`
- Neo4j：本机 `2026.03.1`，服务可启动并监听 `7474/7687`
- 图投影：`DEGRADED`；本次未提供 `NEO4J_USERNAME/NEO4J_PASSWORD`，因此 `0` 条变更标记 `APPLIED`，`47` 条保留在可重放 Outbox；`context --source auto` 明确回退 SQLite
- 认证探针：默认 `neo4j/neo4j` 被拒绝；没有修改用户密码或远程连接

结论：SQLite Canon、快照/补丁语义、历史重建、审计、超边数据、上下文与 Markdown 已可执行；Neo4j 连接只差本机用户凭据，不能将本次运行宣称为图投影完成。
