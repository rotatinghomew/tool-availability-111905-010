# 资料约定

原始资料均为本地合成。CSV 使用 UTF-8，首行是字段名。

时间以当地整数小时计，半开区间。`stock` 记录可单用的实体及套件部件。`parts` 给套件要求的实物 ID，`certifications` 指定 entity 能满足的用途、有效区间和允许地点；套件和部件同段不能重复承诺。`movements` 属于不同事件源，unit 是实体，每条事件有可能发生的 lower 至 upper 小时（含端点）；只知区间时不假设确定发生小时。checked_in 只是扫码、accepted 才验收入库可借；dispatched 后来源点不可借。`requests` 记载出借点、用途、期望起止与实际处置；fulfilled、declined、canceled 分别为已交付、拒绝、取消，`reservations` 为已经承诺的实物占用。`work_orders` 是检修或调运方案，proposed 与 accepted 不代表目标点已验收。`amendments` 明确修订哪一条原记录。`routes` 给可调运途径、最短调运时间和适用实物类型，非路线地点不可直接通借。
