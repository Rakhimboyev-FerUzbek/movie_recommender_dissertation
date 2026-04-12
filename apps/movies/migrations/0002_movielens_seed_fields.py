from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="imdb_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="movie",
            name="rating_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="movie",
            name="source",
            field=models.CharField(db_index=True, default="local", max_length=32),
        ),
        migrations.AddField(
            model_name="movie",
            name="source_movie_id",
            field=models.PositiveIntegerField(blank=True, db_index=True, null=True),
        ),
        migrations.AddIndex(
            model_name="movie",
            index=models.Index(fields=["source", "source_movie_id"], name="movies_movie_source__2bc5e6_idx"),
        ),
    ]