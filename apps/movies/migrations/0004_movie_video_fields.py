from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0003_rename_movies_movie_source__2bc5e6_idx_movies_movi_source_78141e_idx"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="full_video_file",
            field=models.FileField(blank=True, null=True, upload_to="movies/full/"),
        ),
        migrations.AddField(
            model_name="movie",
            name="full_video_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="movie",
            name="trailer_site",
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name="movie",
            name="trailer_url",
            field=models.URLField(blank=True),
        ),
    ]