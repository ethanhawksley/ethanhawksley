import datetime
import json
import re
import urllib.request

feed_url = 'https://hawksley.dev/feed.json'
request = urllib.request.Request(feed_url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(request) as response:
    response_data = response.read().decode('utf-8')
    feed = json.loads(response_data)

new_blog_lines = []
all_posts = feed.get('items', [])
top_two_posts = all_posts[:2]

for post in top_two_posts:
    title = post['title']
    url = post['url']
    summary = post['summary']

    formatted_post = f"- **[{title}]({url})**<br/>{summary}"
    new_blog_lines.append(formatted_post)

post_count = len(all_posts)
view_all_link = f"[View all posts ({post_count})](https://hawksley.dev/blog/)"

posts_text = '\n\n'.join(new_blog_lines)
replacement_text = '\n' + posts_text + '\n\n' + view_all_link + '\n'

with open('README.md', 'r', encoding='utf-8') as file:
    readme_content = file.read()

blog_pattern = r'(<!-- BLOG_START -->).*?(<!-- BLOG_END -->)'
readme_content = re.sub(
    blog_pattern,
    r'\1' + replacement_text + r'\2',
    readme_content,
    flags=re.DOTALL
)

current_week = datetime.date.today().isocalendar()[1]

week_pattern = r'(<!-- WEEK: )\d+( -->)'
readme_content = re.sub(
    week_pattern,
    r'\g<1>' + str(current_week) + r'\g<2>',
    readme_content
)

with open('README.md', 'w', encoding='utf-8') as file:
    file.write(readme_content)
