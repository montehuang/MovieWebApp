#coding:utf8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:0270@127.0.0.1:3306/movie?charset=utf8"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

#会员
class User(db.Model):
	"""会员数据结构"""
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True)
	pwd = db.Column(db.String(100), unique = True)
	email = db.Column(db.String(100), unique = True)
	phone = db.Column(db.String(11), unique = True)
	info = db.Column(db.Text)
	face = db.Column(db.String(255), unique = True)
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	uuid = db.Column(db.String(255), unique = True)
	userlogs = db.relationship("UserLog", backref = "user")
	comments = db.relationship("Comment", backref = "user")
	moviecols = db.relationship("Moviecol", backref = "user")
	admins = db.relationship("Admin", backref = "user")

	def __repr__(self):
		return "<User %r>" % self.name

#会员登陆信息
class UserLog(db.Model):
	__tablename__ = "userlog"
	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	ip = db.Column(db.String(100))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Userlog %r>" % self.id

#标签
class Tag(db.Model):
	__tablename__ = "tag"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True)
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	movies = db.relationship("Movie", backref = "tag")

	def __repr__(self):
		return "<Tag %r>" % self.name

#电影
class Movie(db.Model):
	__tablename__ = "movie"
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(255), unique = True)
	url = db.Column(db.String(255), unique = True)
	info = db.Column(db.Text)
	logo = db.Column(db.String(255), unique = True)
	star = db.Column(db.SmallInteger)
	playnum = db.Column(db.BigInteger)
	commentnum = db.Column(db.BigInteger)
	tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
	area = db.Column(db.String(255))
	release_time = db.Column(db.Date)
	length = db.Column(db.String(100))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	comments = db.relationship("Comment", backref = "movie")
	moviecols = db.relationship("Moviecol", backref = "movie")

	def __repr__(self):
		return "<Movie %r>" % self.title

#预告
class Preview(db.Model):
	"""电影预报"""
	__tablename__ = "preview"
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(255), unique = True)
	logo = db.Column(db.String(255), unique = True)
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Preview %r>" % self.title

#评论
class Comment(db.Model):
	"""电影评论"""
	__tablename__ = "comment"
	id = db.Column(db.Integer, primary_key = True)
	content = db.Column(db.Text)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Comment %r>" % self.id

#电影收藏
class Moviecol(db.Model):
	"""电影收藏"""
	__tablename__ = "moviecol"
	id = db.Column(db.Integer, primary_key = True)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Moviecol %r>" % self.id

#权限
class Auth(db.Model):
	"""权限"""
	__tablename__ = "auth"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True)
	url = db.Column(db.String(255), unique = True)
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Auth %r>" % self.name

#角色
class Role(db.Model):
	"""角色"""
	__tablename__ = "role"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True)
	auths = db.Column(db.String(600))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Role %r>" % self.name

#管理员
class Admin(db.Model):
	__tablename__ = "admin"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), unique = True)
	pwd = db.Column(db.String(100), unique = True)
	is_super = db.Column(db.SmallInteger)
	role_id = db.Column(db.Integer, db.ForeignKey('role.id')) 
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	adminlogs = db.relationship("AdminLog", backref = "admin")
	oplogs = db.relationship("Oplog", backref = "admin")

	def __repr__(self):
		return "<Admin %r>" % self.name

#管理员日志
class AdminLog(db.Model):
	__tablename__ = "adminlog"
	id = db.Column(db.Integer, primary_key = True)
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
	ip = db.Column(db.String(100))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Adminlog %r>" % self.id

#操作日志
class Oplog(db.Model):
	__tablename__ = "oplog"
	id = db.Column(db.Integer, primary_key = True)
	admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
	ip = db.Column(db.String(100))
	reason = db.Column(db.String(600))
	addtime = db.Column(db.DateTime, index = True, default = datetime.utcnow)

	def __repr__(self):
		return "<Oplog %r>" % self.id

if __name__ == "__main__":
	db.create_all()