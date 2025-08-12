#!/bin/bash

# 检查参数数量
if [ $# -ne 2 ]; then
    echo "用法: $0 <搜索文件> <搜索内容>"
    echo "示例: $0 example.txt '要搜索的内容'"
    exit 1
fi

search_file="$1"
search_content="$2"
output_file="search_results_$(date +%Y%m%d_%H%M%S).txt"

# 检查文件是否存在
if [ ! -f "$search_file" ]; then
    echo "错误: 文件 '$search_file' 不存在"
    exit 1
fi

# 执行搜索并处理结果
echo "正在文件 '$search_file' 中搜索 '$search_content'..."
echo "搜索结果将显示在控制台并保存到 '$output_file'"
echo ""

# 搜索并格式化输出
grep -n "$search_content" "$search_file" | while read -r line; do
    # 提取行号和内容
    line_number=$(echo "$line" | cut -d: -f1)
    line_content=$(echo "$line" | cut -d: -f2-)
    
    # 格式化输出
    result="行号 $line_number: $line_content"
    
    # 输出到控制台
    echo "$result"
    
    # 写入文件
    echo "$result" >> "$output_file"
done

# 统计结果
match_count=$(grep -c "$search_content" "$search_file")
echo ""
echo "搜索完成！共找到 $match_count 处匹配。"
echo "详细结果已保存到 $output_file"