from django.db import models
from django.urls import reverse
from django.conf import settings
import re

# Create your models here.

def _get_slug(self, words):
    split_words = re.split('[\W]+', words)
    slug = []
    slugify = ''
    for word in split_words:
        if word:
            slug.append(word)
    slugify = '-'.join(slug)
    return slugify


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True, unique=True, allow_unicode=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug(name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:post_list_by_category', args=[self.slug])


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    # 'auth.User' 엡이름.모델
    # setting.AUTH_USER_MODEL: 사용자 인증에 사용되는 User모델이 변경됐을 경우 자동 대응
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # Tag 클래스로 지정 or 'Tag' 문자열 형태로 걸 수 있다 그러면 Tag모델이 post 뒤에 있어도 사용할 수 있다.
    # manytomany일 경우 blank option을 선호
    Tags = models.ManyToManyField('Tag', blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True)
    Comments = models.PositiveSmallIntegerField(default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='post/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ['-created']
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.title

    def publish(self):
        self.published = timezone.now()
        self.save()

    def _get_slug(self):
        split_title = re.split('[\W]+', self.title)
        slug = []
        slugify = ''
        for word in split_title:
            if word:
                slug.append(word)
        slugify = '-'.join(slug)
        return slugify

    def save_tags(self):
        if not tag:
            return 
        
        tags_list = []
        # 입력된 값들을 # 구분자로 구분한 후 공백 제거
        tags = map(lambda str: str.strip(), unicode(tags).split('#'))
        # TagModel DB에서 입력된 값들을 가져오거나 없으면 생성
        for tag in tags:
            tag = Tags.objects.get_or_create(name=tag)[0]
            self.Tags.add(tag)
        # tags_list = [TagModel.objects.get_or_create(name=tag)[0] for tag in tags]
        # # Tags를 리스트 형태로 반환
        # self.Tag.add(*tag_list)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_slug()
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug, self.id])


class Comment(models.Model):
    post = models.ForeignKey('post', on_delete=models.CASCADE, related_name='comments', null=False)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length=32, null=False)
    content = models.TextField(max_length=2000, null=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        self.content