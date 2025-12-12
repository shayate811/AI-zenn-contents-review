import os
import sys
import glob
import anthropic

# 記事のスタイル定義（Zenn風など、好みに合わせて調整）
SYSTEM_PROMPT = """
あなたは優秀な技術記事の編集者です。
渡されたMarkdown形式の技術記事をレビューし、以下の点を改善した「修正版」を出力してください。

1. 誤字脱字の修正
2. "です・ます"調への統一（技術記事として自然なトーン）
3. 読みにくい文章の構造化（箇条書きの活用など）
4. 初心者にもわかりやすい補足説明の追加（必要な場合）

出力はMarkdownの本文のみを行ってください。余計な挨拶や説明は不要です。
"""

def review_article(file_path):
    client = anthropic.Anthropic(
        api_key=os.environ.get("ANTHROPIC_API_KEY"),
    )

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Reviewing: {file_path} ...")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=8000,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": f"以下のMarkdown記事を校正してください:\n\n{content}"}
        ]
    )

    reviewed_content = message.content[0].text

    # 上書き保存（Gitで差分管理するので大胆に上書きしてOK）
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(reviewed_content)

if __name__ == "__main__":
    # 引数で渡されたファイルリスト、または特定のディレクトリ配下のmdを対象にする
    files = sys.argv[1:]
    
    if not files:
        print("No files to review.")
        sys.exit(0)

    for file in files:
        if file.endswith(".md"):
            review_article(file)