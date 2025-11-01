from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_item_itemgroup_unit_remove_quotationitem_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quotationitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.item'),
        ),
        migrations.AlterField(
            model_name='quotationtemplateitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.item'),
        ),
    ]