from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_userprofile_gender"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="previous_last_login",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]