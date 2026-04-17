from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_userprofile_birth_date_phone_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="birth_year",
        ),
    ]