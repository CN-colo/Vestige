"""数据库迁移脚本 - 添加社交功能相关字段和表"""
import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'vestige.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("开始数据库迁移...")

# 1. 添加 like_count 列到 articles 表
try:
    cursor.execute('ALTER TABLE articles ADD COLUMN like_count INTEGER DEFAULT 0')
    print('✓ Added like_count to articles')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('✓ articles.like_count already exists')
    else:
        print(f'! articles: {e}')

# 2. 添加 like_count 列到 projects 表
try:
    cursor.execute('ALTER TABLE projects ADD COLUMN like_count INTEGER DEFAULT 0')
    print('✓ Added like_count to projects')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('✓ projects.like_count already exists')
    else:
        print(f'! projects: {e}')

# 3. 创建 follows 表
try:
    cursor.execute('''
        CREATE TABLE follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_id INTEGER NOT NULL,
            following_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (follower_id) REFERENCES users (id),
            FOREIGN KEY (following_id) REFERENCES users (id),
            UNIQUE (follower_id, following_id)
        )
    ''')
    print('✓ Created follows table')
except sqlite3.OperationalError as e:
    if 'table already exists' in str(e):
        print('✓ follows table already exists')
    else:
        print(f'! follows: {e}')

# 4. 创建 tag_subscriptions 表
try:
    cursor.execute('''
        CREATE TABLE tag_subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            tag VARCHAR(50) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, tag)
        )
    ''')
    print('✓ Created tag_subscriptions table')
except sqlite3.OperationalError as e:
    if 'table already exists' in str(e):
        print('✓ tag_subscriptions table already exists')
    else:
        print(f'! tag_subscriptions: {e}')

# 5. 创建 likes 表
try:
    cursor.execute('''
        CREATE TABLE likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            target_type VARCHAR(20) NOT NULL,
            target_id INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            UNIQUE (user_id, target_type, target_id)
        )
    ''')
    print('✓ Created likes table')
except sqlite3.OperationalError as e:
    if 'table already exists' in str(e):
        print('✓ likes table already exists')
    else:
        print(f'! likes: {e}')

# 6. 添加 content 列到 projects 表（正文内容）
try:
    cursor.execute('ALTER TABLE projects ADD COLUMN content TEXT')
    print('✓ Added content to projects')
except sqlite3.OperationalError as e:
    if 'duplicate column name' in str(e):
        print('✓ projects.content already exists')
    else:
        print(f'! projects content: {e}')

conn.commit()
conn.close()

print("\n数据库迁移完成!")