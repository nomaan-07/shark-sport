from db import Base, relationship
from sqlalchemy import Column, ForeignKey , VARCHAR, Integer, TIMESTAMP, Boolean

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(100))
    #relationships
    products = relationship('ProductTag', back_populates='tag')
    articles = relationship('ArticleTag', back_populates='tag')


class ProductTag(Base):
    __tablename__ = 'product_tag'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), primary_key=True)
    #relationships
    product = relationship('Product', back_populates='tags')
    tag = relationship('Tag', back_populates='products')

class ArticleTag(Base):
    __tablename__ = 'article_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey('tag.id'), nullable=False)
    article_id = Column(Integer, ForeignKey('articles.id'), nullable=False)
    #relationships
    article = relationship('Article', back_populates='article_tags')
    tag = relationship('Tag', back_populates='articles')