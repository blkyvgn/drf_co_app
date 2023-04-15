from django.db import models
from django.conf import settings
from api.vendors.base.model import BaseModel
from api.vendors.helpers.translation import tr
from django.contrib.auth import get_user_model
from django.utils.translation import get_language
from ckeditor_uploader.fields import RichTextUploadingField
from api.vendors.mixins.model import (
	SoftdeleteMixin, 
	TimestampsMixin,
	ImgMixin,
	HelpersMixin,
)
Account = get_user_model()

def article_thumb_upload_to(instance, filename):
	return f'company/{instance.company}/articles/{instance.slug}/thumb/{filename}'

class Article(BaseModel, ImgMixin, HelpersMixin, TimestampsMixin):
	slug = models.SlugField(
		max_length=250,
	)
	thumb = models.ImageField(
		upload_to=article_thumb_upload_to, 
		null=True,
		blank=True,
	)
	category = models.ForeignKey(
		'Category',
		related_name='articles',
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
	)
	author = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='articles',
		default=1,
	)
	created_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='article_creator',
		null=True,
		blank=True,
	)
	updated_by = models.ForeignKey(
		Account, 
		on_delete=models.CASCADE, 
		related_name='article_updater', 
		null=True,
		blank=True,
	)
	tags = models.ManyToManyField(
		'Tag',
		related_name='article_tags',
	)
	company = models.ForeignKey(
		'company.Company',
		on_delete=models.CASCADE, 
		related_name='articles',
	)

	def __str__(self):
		return self.slug

	class Meta:
		verbose_name = tr('article')
		verbose_name_plural = tr('articles')
		constraints = [
			models.UniqueConstraint(fields=['company_id', 'slug'], name='unique_article_slug')
		]
		indexes = [
			models.Index(fields=('company_id', 'slug')),
		]

	raw_queries = {
		'out_list': '''SELECT "article_article"."id",
				"C"."username" AS "owner", 
				"category_category"."name" AS "cat", 
				"article_articlebody"."name" AS "name", 
				COUNT("article_comment"."id") AS "comments_count", 
				GROUP_CONCAT(DISTINCT "B"."lang") AS "langs" 
			FROM "article_article" 
			INNER JOIN "account_account" AS "C"
				ON ("article_article"."author_id" = "C"."id") 
			LEFT OUTER JOIN "category_category" 
				ON ("article_article"."category_id" = "category_category"."id") 
			LEFT OUTER JOIN "article_articlebody" AS "B"
				ON ("article_article"."id" = "B"."article_id")
			LEFT OUTER JOIN "article_articlebody" 
				ON ("article_article"."id" = "article_articlebody"."article_id") 
					AND ("article_articlebody"."lang"=%s)
			LEFT OUTER JOIN "article_comment" 
				ON ("article_article"."id" = "article_comment"."article_id") 
			WHERE (NOT "article_article"."is_blocked" AND "article_article"."is_shown") 
			GROUP BY "article_article"."id"
			ORDER BY "article_article"."created_at" DESC'''
	}



class ArticleBody(models.Model):
	name = models.CharField(
		max_length=250, 
		null=True, 
		blank=True,
	)
	short_desc = RichTextUploadingField(
		max_length=600, 
		null=True, 
		blank=True,
	)
	content = RichTextUploadingField(
		null=True, 
		blank=True,
	)
	lang = models.CharField(
		max_length=5,
		default=settings.LANGUAGE_CODE,
	)
	article = models.ForeignKey(
		Article, 
		related_name='body', 
		on_delete=models.CASCADE,
	)