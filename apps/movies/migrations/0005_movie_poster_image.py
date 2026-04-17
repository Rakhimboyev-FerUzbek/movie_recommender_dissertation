from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("movies", "0004_movie_metadata_enrichment"),
    ]

    operations = [
        migrations.AddField(
            model_name="movie",
            name="poster_image",
            field=models.ImageField(blank=True, null=True, upload_to="movies/posters/"),
        ),
    ]