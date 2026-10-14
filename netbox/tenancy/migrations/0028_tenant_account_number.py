from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenancy', '0027_fix_ltree_cascade_triggers'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='account_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='account number'),
        ),
    ]
