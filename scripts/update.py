import urllib.request, json, re, datetime

req = urllib.request.Request('https://hawksley.dev/feed.json', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
  feed = json.loads(response.read().decode('utf-8'))

lines = []
for post in feed.get('items', [])[:2]:
  title, url, summary = post['title'], post['url'], post['summary']
  lines.append(f'- **[{title}]({url})**<br/>{summary}')

replacement = '\n' + '\n\n'.join(lines) + '\n'

with open('README.md', 'r', encoding='utf-8') as f:
  content = f.read()

pattern = r'(<!-- BLOG_START -->).*?(<!-- BLOG_END -->)'
content = re.sub(pattern, r'\1' + replacement + r'\2', content, flags=re.DOTALL)

week_num = datetime.date.today().isocalendar()[1]
content = re.sub(r'(<!-- WEEK: )\d+( -->)', r'\g<1>' + str(week_num) + r'\g<2>', content)


with open('README.md', 'w', encoding='utf-8') as f:
  f.write(content)
