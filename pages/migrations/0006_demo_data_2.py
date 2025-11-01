from django.db import migrations

def create_demo_data(apps, schema_editor):
    QuotationTemplate = apps.get_model('pages', 'QuotationTemplate')
    QuotationTemplateItem = apps.get_model('pages', 'QuotationTemplateItem')

    template1 = QuotationTemplate.objects.create(name='Template A')
    QuotationTemplateItem.objects.create(template=template1, group_name='Part A', description='Item A1', qty=1, unit='pcs', unit_price=100)
    QuotationTemplateItem.objects.create(template=template1, group_name='Part A', description='Item A2', qty=2, unit='pcs', unit_price=200)
    QuotationTemplateItem.objects.create(template=template1, group_name='Part B', description='Item B1', qty=3, unit='pcs', unit_price=300)

    template2 = QuotationTemplate.objects.create(name='Template B')
    QuotationTemplateItem.objects.create(template=template2, group_name='Part C', description='Item C1', qty=1, unit='pcs', unit_price=150)
    QuotationTemplateItem.objects.create(template=template2, group_name='Part C', description='Item C2', qty=2, unit='pcs', unit_price=250)


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_demo_data'),
    ]

    operations = [
        migrations.RunPython(create_demo_data),
    ]