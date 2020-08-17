# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    wid = models.CharField(max_length=20)
    time = models.DateTimeField(blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    like_count = models.IntegerField(blank=True, null=True)
    uid = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    following = models.IntegerField(blank=True, null=True)
    followed = models.IntegerField(blank=True, null=True)
    pro_url = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'
        unique_together = (('id', 'wid'),)


class Follow(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    id = models.CharField(max_length=20)
    screen_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follow'
        unique_together = (('user_id', 'id'),)


class Pr(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    pr = models.CharField(db_column='PR', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pr'


class Sensitivity(models.Model):
    id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'sensitivity'


class Topic(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    bid = models.CharField(max_length=12)
    user_id = models.CharField(max_length=20, blank=True, null=True)
    screen_name = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    article_url = models.CharField(max_length=100, blank=True, null=True)
    topics = models.CharField(max_length=200, blank=True, null=True)
    at_users = models.CharField(max_length=1000, blank=True, null=True)
    pics = models.CharField(max_length=3000, blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=30, blank=True, null=True)
    attitudes_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    retweet_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    screen_name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    statuses_count = models.IntegerField(blank=True, null=True)
    followers_count = models.IntegerField(blank=True, null=True)
    follow_count = models.IntegerField(blank=True, null=True)
    registration_time = models.CharField(max_length=20, blank=True, null=True)
    sunshine = models.CharField(max_length=20, blank=True, null=True)
    birthday = models.CharField(max_length=40, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    education = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=140, blank=True, null=True)
    profile_url = models.CharField(max_length=200, blank=True, null=True)
    profile_image_url = models.CharField(max_length=200, blank=True, null=True)
    avatar_hd = models.CharField(max_length=200, blank=True, null=True)
    urank = models.IntegerField(blank=True, null=True)
    mbrank = models.IntegerField(blank=True, null=True)
    verified = models.IntegerField(blank=True, null=True)
    verified_type = models.IntegerField(blank=True, null=True)
    verified_reason = models.CharField(max_length=140, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'


class Weibo(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    bid = models.CharField(max_length=12)
    user_id = models.CharField(max_length=20, blank=True, null=True)
    screen_name = models.CharField(max_length=30, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    article_url = models.CharField(max_length=100, blank=True, null=True)
    topics = models.CharField(max_length=200, blank=True, null=True)
    at_users = models.CharField(max_length=1000, blank=True, null=True)
    pics = models.CharField(max_length=3000, blank=True, null=True)
    video_url = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=30, blank=True, null=True)
    attitudes_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    retweet_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weibo'
