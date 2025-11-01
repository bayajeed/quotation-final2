from django.db import migrations

def create_demo_data(apps, schema_editor):
    QuotationTemplate = apps.get_model('pages', 'QuotationTemplate')
    QuotationTemplateItem = apps.get_model('pages', 'QuotationTemplateItem')

    # Template 1
    template1 = QuotationTemplate.objects.create(name='Standard Quotation')
    QuotationTemplateItem.objects.create(template=template1, group_name='Part A', description='Item A1', qty=1, unit='Pcs', unit_price=100)
    QuotationTemplateItem.objects.create(template=template1, group_name='Part A', description='Item A2', qty=2, unit='Pcs', unit_price=150)
    QuotationTemplateItem.objects.create(template=template1, group_name='Part B', description='Item B1', qty=1, unit='Pcs', unit_price=200)

    # Template 2
    template2 = QuotationTemplate.objects.create(name='Advanced Quotation')
    QuotationTemplateItem.objects.create(template=template2, group_name='Part A', description='Advanced Item A1', qty=1, unit='Pcs', unit_price=120)
    QuotationTemplateItem.objects.create(template=template2, group_name='Part B', description='Advanced Item B1', qty=2, unit='Pcs', unit_price=180)
    QuotationTemplateItem.objects.create(template=template2, group_name='Part C', description='Advanced Item C1', qty=1, unit='Pcs', unit_price=250)

class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_quotation_total_amount_and_more'),
    ]

    operations = [
        migrations.RunPython(create_demo_data),
    ]