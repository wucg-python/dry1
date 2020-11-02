from django.db import models

# Create your models here.


# 抽象类，数据库中不显示该模型
# 其他模型继承该模型，继承该模型中的字段
class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Book(BaseModel):
    book_name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5,decimal_places=2)
    pic = models.ImageField(upload_to='pic',default='pic/1.jpg')
    author = models.ManyToManyField(to='Author',db_constraint=False, related_name="books")
    publish = models.ForeignKey(to="Publisher",on_delete=models.CASCADE,db_constraint=False,related_name='books')

    class Meta:
        db_table = "book"
        verbose_name = "书籍"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.book_name

    # 在序列化的模型中自定义序列化属性
    # 方法属性
    @property
    def pub_name(self):
        print(self.publish)
        return self.publish.pub_name

    @property
    def authors(self):
        print(self.author)
        return self.author.values("author_name","age")

class Author(BaseModel):
    author_name = models.CharField(max_length=20)
    age = models.IntegerField()

    class Meta:
        db_table = "author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name

class Publisher(BaseModel):
    pub_name = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='pic',default='pic/2.jpg')
    address = models.CharField(max_length=100)

    class Meta:
        db_table = "publisher"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pub_name

class User(BaseModel):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    class Meta:
        db_table = "user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name