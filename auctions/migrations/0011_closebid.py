# Generated by Django 3.0.8 on 2020-10-14 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_remove_bid_listingid'),
    ]

    operations = [
        migrations.CreateModel(
            name='closebid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item', to='auctions.createlisting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('win', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='win', to='auctions.createlisting')),
            ],
        ),
    ]
