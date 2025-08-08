import matplotlib as mpl
mpl.use("Agg")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import jieba
from collections import Counter
import matplotlib.font_manager as fm
import os

# 优先使用本地 FontManager 一行初始化，启用 emoji 黑白后备，确保中文/emoji 同时可见
try:
    from font_manager import setup_matplotlib_chinese  # 本仓库提供
    _fm_result = setup_matplotlib_chinese(emoji_fallback=True, emoji_prefer_color=False)
    _wordcloud_font_path_from_fm = None
    if getattr(_fm_result, 'success', False) and getattr(_fm_result, 'font_used', None):
        _wordcloud_font_path_from_fm = getattr(_fm_result.font_used, 'path', None)
except Exception:
    _wordcloud_font_path_from_fm = None

# 作为兜底：简单扫描系统字体，供 WordCloud 使用
def get_chinese_font_path():
    candidates = [
        '/System/Library/Fonts/Hiragino Sans GB.ttc',
        '/System/Library/Fonts/PingFang.ttc',
        '/Library/Fonts/Arial Unicode.ttf',
        '/System/Library/Fonts/STHeiti Medium.ttc',
        '/System/Library/Fonts/STHeiti Light.ttc'
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    for fp in fm.findSystemFonts():
        if any(k in fp.lower() for k in ['hiragino', 'pingfang', 'heiti', 'simhei', 'msyh', 'arial unicode']):
            return fp
    return None

# 数据预处理
print("正在加载数据...")
df = pd.read_csv('/Users/duting/Downloads/命理风水占卜🔮/fixed_twitter_data/specific_keywords_865_20250804_171510.csv')
df['created_at'] = pd.to_datetime(df['created_at'], format='%a %b %d %H:%M:%S %z %Y', errors='coerce')
print(f"数据加载完成，共 {len(df)} 条推文")

# 1. 提取风水相关推文
fengshui_keywords = ['feng shui', '风水', '風水', '家居布局', '家相', '运势', '招财', '辟邪', '五行', '八卦']
pattern = '|'.join(fengshui_keywords)
fengshui_tweets = df[df['text'].str.contains(pattern, case=False, na=False)].copy()
print(f"找到 {len(fengshui_tweets)} 条风水相关推文")

# 2. 主题分类与意图分析
theme_data = {
    '装饰': {'keywords': ['decor', 'decoration', '装饰', '擺設', '摆件', '貔貅', '水晶', 'crystal'],
           'intent': '商业推广', 'color': '#FF7F0E'},
    '家居布局': {'keywords': ['layout', 'arrangement', '布局', '家相', '方位', '户型', 'room'],
              'intent': '实用指南', 'color': '#1F77B4'},
    '运势预测': {'keywords': ['fortune', 'luck', '運勢', '招财', '财运', '八字', '生肖', 'prediction'],
              'intent': '心理安慰', 'color': '#2CA02C'},
    '理论探讨': {'keywords': ['theory', '五行', '八卦', '阴阳', 'energy flow', '争议', 'philosophy'],
              'intent': '文化传播', 'color': '#D62728'}
}

# 3. 主题频率统计
theme_counts = {}
for theme in theme_data:
    theme_counts[theme] = len(fengshui_tweets[fengshui_tweets['text'].str.contains(
        '|'.join(theme_data[theme]['keywords']), case=False, na=False)])

# 4. 可视化设置
plt.style.use('default')
fig = plt.figure(figsize=(18, 20))

# 主题频率分布
plt.subplot(3, 2, 1)
theme_df = pd.DataFrame.from_dict(theme_counts, orient='index', columns=['Count'])
theme_df['Percentage'] = theme_df['Count'] / max(len(fengshui_tweets), 1) * 100
theme_df = theme_df.sort_values('Count', ascending=False)

ax = sns.barplot(x=theme_df.index, y='Count', data=theme_df,
                palette=[theme_data[t]['color'] for t in theme_df.index])
plt.title('风水主题频率分布', fontsize=16, fontweight='bold')
plt.xlabel('主题类别', fontsize=14)
plt.ylabel('推文数量', fontsize=14)
for p in ax.patches:
    ax.annotate(f'{p.get_height()}\n({p.get_height()/max(len(fengshui_tweets),1)*100:.1f}%)',
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=10)

# 主题互动对比
plt.subplot(3, 2, 2)
interaction_data = []
for theme in theme_data:
    theme_tweets = fengshui_tweets[fengshui_tweets['text'].str.contains(
        '|'.join(theme_data[theme]['keywords']), case=False, na=False)]
    if len(theme_tweets) > 0:
        interaction_data.append({
            'Theme': theme,
            'Avg Likes': theme_tweets['like_count'].mean(),
            'Avg Retweets': theme_tweets['retweet_count'].mean(),
            'Avg Replies': theme_tweets['reply_count'].mean(),
            'Intent': theme_data[theme]['intent']
        })
interaction_df = pd.DataFrame(interaction_data)
if len(interaction_df) > 0:
    interaction_df.plot(x='Theme', y=['Avg Likes', 'Avg Retweets', 'Avg Replies'],
                       kind='bar', ax=plt.gca(), color=['#FF7F0E', '#1F77B4', '#2CA02C'])
    plt.title('各主题平均互动量对比', fontsize=16, fontweight='bold')
    plt.xlabel('主题类别', fontsize=14)
    plt.ylabel('平均互动量', fontsize=14)
    plt.xticks(rotation=45)
    plt.legend(title='互动类型')

# 主题时间趋势
plt.subplot(3, 2, (3,4))
fengshui_tweets_with_date = fengshui_tweets.copy()
fengshui_tweets_with_date['date'] = pd.to_datetime(fengshui_tweets_with_date['created_at']).dt.date
trend_data = []
for theme in theme_data:
    theme_tweets = fengshui_tweets_with_date[fengshui_tweets_with_date['text'].str.contains(
        '|'.join(theme_data[theme]['keywords']), case=False, na=False)]
    if len(theme_tweets) > 0:
        trend = theme_tweets.groupby('date').size().reset_index(name='Count')
        trend['Theme'] = theme
        trend_data.append(trend)
if trend_data:
    trend_df = pd.concat(trend_data)
    sns.lineplot(x='date', y='Count', hue='Theme', data=trend_df,
               palette=[theme_data[t]['color'] for t in theme_data], linewidth=2.5)
    plt.title('风水主题时间趋势', fontsize=16, fontweight='bold')
    plt.xlabel('日期', fontsize=14)
    plt.ylabel('每日推文量', fontsize=14)
    plt.legend(title='主题类别')

# 作者类型分析
plt.subplot(3, 2, 5)
author_data = []
for theme in theme_data:
    theme_tweets = fengshui_tweets[fengshui_tweets['text'].str.contains(
        '|'.join(theme_data[theme]['keywords']), case=False, na=False)]
    if len(theme_tweets) > 0:
        commercial = len(theme_tweets[theme_tweets['author_is_verified'] == True])
        personal = len(theme_tweets[theme_tweets['author_is_verified'] == False])
        author_data.extend([
            {'Theme': theme, 'Type': '商业账号', 'Count': commercial},
            {'Theme': theme, 'Type': '个人用户', 'Count': personal}
        ])
author_df = pd.DataFrame(author_data)
if len(author_df) > 0:
    sns.barplot(x='Theme', y='Count', hue='Type', data=author_df,
               palette=['#9467BD', '#8C564B'])
    plt.title('各主题作者类型分布', fontsize=16, fontweight='bold')
    plt.xlabel('主题类别', fontsize=14)
    plt.ylabel('推文数量', fontsize=14)
    plt.legend(title='账号类型')

# 语言分布分析
plt.subplot(3, 2, 6)
lang_data = []
for theme in theme_data:
    theme_tweets = fengshui_tweets[fengshui_tweets['text'].str.contains(
        '|'.join(theme_data[theme]['keywords']), case=False, na=False)]
    if len(theme_tweets) > 0:
        lang_counts = theme_tweets['language'].value_counts().head(3)
        for lang, count in lang_counts.items():
            lang_data.append({'Theme': theme, 'Language': lang, 'Count': count})
lang_df = pd.DataFrame(lang_data)
if len(lang_df) > 0:
    sns.barplot(x='Theme', y='Count', hue='Language', data=lang_df,
               palette=['#E377C2', '#7F7F7F', '#BCBD22'])
    plt.title('各主题语言分布(Top3)', fontsize=16, fontweight='bold')
    plt.xlabel('主题类别', fontsize=14)
    plt.ylabel('推文数量', fontsize=14)
    plt.legend(title='语言')

plt.tight_layout()
plt.savefig('/Users/duting/Downloads/命理风水占卜🔮/爬虫分析图表/风水主题分析图表.png', 
            dpi=300, bbox_inches='tight')
# plt.show()  # 非交互环境不显示
plt.close()

# 词云分析
def chinese_word_segmentation(text):
    """中文分词处理"""
    try:
        seg_list = jieba.cut(str(text), cut_all=False)
        return ' '.join(seg_list)
    except:
        return str(text)

print("正在生成词云...")
all_text = ' '.join(fengshui_tweets['text'].astype(str))
all_text = chinese_word_segmentation(all_text)

font_path = get_chinese_font_path()
wordcloud_kwargs = dict(width=1000, height=500, background_color='white', collocations=False, max_words=100)
if font_path:
    wordcloud_kwargs['font_path'] = font_path
wordcloud = WordCloud(**wordcloud_kwargs).generate(all_text)

plt.figure(figsize=(15, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('风水主题关键词词云', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/duting/Downloads/命理风水占卜🔮/爬虫分析图表/风水主题词云.png', 
            dpi=300, bbox_inches='tight')
# plt.show()
plt.close()

print("✅ 风水主题分析完成！")
print(f"📊 生成了 {len(fengshui_tweets)} 条风水相关推文的分析")
print(f"📁 图表已保存到: /Users/duting/Downloads/命理风水占卜🔮/爬虫分析图表/")