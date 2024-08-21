from database import db
from datetime import datetime
import pytz   # 导入 pytz 以处理时区

class Documents(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')), nullable=False)
    is_favorite = db.Column(db.Boolean, default=False)  # 表示文档是否被收藏
    is_deleted = db.Column(db.Boolean, default=False)  # 表示文档是否被逻辑删除
    is_template = db.Column(db.Boolean, default=False)  # 表示文档是否为模板

    def __repr__(self):
        return '<Document %r>' % self.title

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
