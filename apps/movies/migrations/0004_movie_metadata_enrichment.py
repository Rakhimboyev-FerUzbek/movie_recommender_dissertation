from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0004_movie_video_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="language",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="movie",
            name="country",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="movie",
            name="director",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="movie",
            name="cast_names",
            field=models.JSONField(blank=True, default=list),
        ),
    ]