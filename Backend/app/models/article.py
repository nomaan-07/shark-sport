from db import Base, relationship
from sqlalchemy import ForeignKey, Column, Integer, TIMESTAMP, VARCHAR

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=False)
    author = Column(VARCHAR(100), nullable=False)
    tags = Column(VARCHAR(255))
    description = Column(VARCHAR(5000))
    created_at = Column(TIMESTAMP, nullable=False)
    modified_at = Column(TIMESTAMP)
    #relationships
    favorite_articles = relationship('UserFavoriteArticle', back_populates='article')
    article_tags = relationship('ArticleTag', back_populates='article')

class UserFavoriteArticle(Base):
    __tablename__ = 'user_favorite_articles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    #relationships
    user = relationship('User', back_populates='favorite_articles')
    article = relationship('Article', back_populates='favorite_articles')