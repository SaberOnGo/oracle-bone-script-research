# AI Agent Research Assistant Design / AI Agent 研究助手设计

English:
The AI Agent should retrieve evidence before reasoning. It should not guess from memory or present unsupported decipherment claims.

简体中文：
AI Agent 应先检索证据，再进行推理。不得凭记忆猜测，也不得给出缺乏证据支持的释读结论。

## Workflow / 工作流

```text
unknown glyph or character ID
  -> source and asset lookup
  -> inscription context lookup
  -> component and variant lookup
  -> co-occurrence and distribution lookup
  -> scholarly argument lookup
  -> evidence pack
  -> hypothesis with support, objections, and next checks
```

```text
未知字或甲骨字 ID
  -> 来源和资产检索
  -> 卜辞上下文检索
  -> 构件和变体检索
  -> 共现和分布检索
  -> 学术论证检索
  -> evidence pack
  -> 输出包含支持证据、反对证据和待验证事项的假说
```
