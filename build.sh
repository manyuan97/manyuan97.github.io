#!/bin/bash
# 自动构建脚本：生成 HTML 并注入访客统计代码

cd "$(dirname "$0")"

# 1. 用 jemdoc 生成 HTML
python3 jemdoc.py index.jemdoc
echo "✅ jemdoc 生成完成"

# 2. 在 </body> 前注入 MapMyVisitors 统计脚本
if grep -q "mapmyvisitors" index.html; then
  echo "ℹ️  统计代码已存在，跳过注入"
else
  sed -i '' 's|</body>|<script type="text/javascript" id="mapmyvisitors" src="//mapmyvisitors.com/map.js?d=A5xDGc_wZOf0OFNs-6UudWghfSkX4Cw10a4tMaBBNxE\&cl=ffffff\&w=a"></script>\
</body>|' index.html
  echo "✅ 访客统计代码注入完成"
fi

echo "🎉 构建完成！"
